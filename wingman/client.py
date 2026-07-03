import logging
import time
from typing import Any

from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from wingman.config import Settings, get_settings
from wingman.prompt import build_messages
from wingman.safety import build_safety_response, check_input_safety, check_output_safety
from wingman.schema import WingmanResponse, WingmanResult, extract_json_object, normalize_wingman_data

logger = logging.getLogger(__name__)


class WingmanClient:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            if not self.settings.deepseek_api_key:
                raise ValueError(
                    "DEEPSEEK_API_KEY is not set. Copy .env.example to .env and add your key."
                )
            self._client = OpenAI(
                api_key=self.settings.deepseek_api_key,
                base_url=self.settings.deepseek_base_url,
            )
        return self._client

    def is_configured(self) -> bool:
        return bool(self.settings.deepseek_api_key)

    @retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=1, max=4))
    def _call_api(self, messages: list[dict[str, str]]) -> tuple[str, int, int, float]:
        start = time.perf_counter()
        kwargs: dict[str, Any] = {
            "model": self.settings.deepseek_model,
            "messages": messages,
            "temperature": self.settings.wingman_temperature,
            "max_tokens": self.settings.wingman_max_tokens,
            "response_format": {"type": "json_object"},
        }
        try:
            completion = self.client.chat.completions.create(
                **kwargs,
                extra_body={"thinking": {"type": "disabled"}},
            )
        except Exception:
            completion = self.client.chat.completions.create(**kwargs)
        latency_ms = (time.perf_counter() - start) * 1000

        content = completion.choices[0].message.content or ""
        usage = completion.usage
        input_tokens = usage.prompt_tokens if usage else 0
        output_tokens = usage.completion_tokens if usage else 0

        return content, input_tokens, output_tokens, latency_ms

    def generate(
        self,
        user_input: str,
        *,
        relationship_stage: str | None = None,
        user_emotion: str | None = None,
        cache_hit: bool = False,
    ) -> WingmanResult:
        is_unsafe, reason = check_input_safety(user_input)
        if is_unsafe:
            payload = build_safety_response(reason or "unsafe")
            response = WingmanResponse(
                mode=payload["mode"],
                energy_read=payload["energy_read"],
                wingman_response=payload["wingman_response"],
                suggested_messages=payload.get("suggested_messages") or ["(no message, situation needs boundaries)"],
                follow_up_question=None,
                safety_flag=True,
                confidence=payload["confidence"],
            )
            return WingmanResult(
                response=response,
                latency_ms=0.0,
                model=self.settings.deepseek_model,
            )

        messages = build_messages(
            user_input,
            relationship_stage=relationship_stage,
            user_emotion=user_emotion,
        )

        raw_content = ""
        input_tokens = output_tokens = 0
        latency_ms = 0.0
        last_error: Exception | None = None

        for attempt in range(2):
            try:
                raw_content, input_tokens, output_tokens, latency_ms = self._call_api(messages)
                data = normalize_wingman_data(extract_json_object(raw_content))
                response = WingmanResponse.model_validate(data)

                if check_output_safety(
                    response.wingman_response + " ".join(response.suggested_messages)
                ):
                    response.safety_flag = True

                cost = self._estimate_cost(input_tokens, output_tokens, cache_hit=cache_hit)

                return WingmanResult(
                    response=response,
                    latency_ms=latency_ms,
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    estimated_cost_usd=cost,
                    model=self.settings.deepseek_model,
                    raw_content=raw_content,
                )
            except Exception as exc:
                last_error = exc
                logger.warning("Wingman generation attempt %s failed: %s", attempt + 1, exc)
                err_text = str(exc).lower()
                if "insufficient balance" in err_text or "402" in err_text:
                    raise RuntimeError(
                        "DeepSeek API returned Insufficient Balance. "
                        "Top up at https://platform.deepseek.com then retry."
                    ) from exc
                if attempt == 0:
                    messages = messages + [
                        {
                            "role": "user",
                            "content": "Your last response was invalid. Return ONLY valid JSON matching the schema.",
                        }
                    ]

        raise RuntimeError(f"Failed to generate Wingman response: {last_error}") from last_error

    def _estimate_cost(
        self,
        input_tokens: int,
        output_tokens: int,
        *,
        cache_hit: bool,
    ) -> float:
        input_rate = (
            self.settings.price_cache_hit_per_million
            if cache_hit
            else self.settings.price_input_per_million
        )
        return (
            input_tokens * input_rate / 1_000_000
            + output_tokens * self.settings.price_output_per_million / 1_000_000
        )

    def estimate_cost_per_1000(
        self,
        avg_input_tokens: int = 1800,
        avg_output_tokens: int = 250,
        *,
        cache_hit: bool = True,
    ) -> float:
        input_rate = (
            self.settings.price_cache_hit_per_million
            if cache_hit
            else self.settings.price_input_per_million
        )
        per_reply = (
            avg_input_tokens * input_rate / 1_000_000
            + avg_output_tokens * self.settings.price_output_per_million / 1_000_000
        )
        return per_reply * 1000
