import json
import re
from typing import Any

from pydantic import BaseModel, Field, field_validator


class WingmanResponse(BaseModel):
    mode: str = Field(default="reply_suggestion")
    energy_read: str
    wingman_response: str
    suggested_messages: list[str] = Field(min_length=1, max_length=3)
    follow_up_question: str | None = None
    safety_flag: bool = False
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator("suggested_messages")
    @classmethod
    def strip_messages(cls, messages: list[str]) -> list[str]:
        cleaned = [m.strip() for m in messages if m and m.strip()]
        if not cleaned:
            raise ValueError("suggested_messages must contain at least one non-empty string")
        return cleaned[:3]

    @field_validator("follow_up_question")
    @classmethod
    def normalize_follow_up(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        if not stripped or stripped.lower() in {"null", "none", "n/a"}:
            return None
        return stripped

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "energy_read": self.energy_read,
            "wingman_response": self.wingman_response,
            "suggested_messages": self.suggested_messages,
            "follow_up_question": self.follow_up_question,
            "safety_flag": self.safety_flag,
            "confidence": round(self.confidence, 2),
        }


class WingmanResult(BaseModel):
    response: WingmanResponse
    latency_ms: float
    input_tokens: int = 0
    output_tokens: int = 0
    estimated_cost_usd: float = 0.0
    model: str = ""
    raw_content: str | None = None


def extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    if not text:
        raise ValueError("Empty model response")

    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in model response") from None
        return json.loads(text[start : end + 1])


def normalize_wingman_data(data: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(data)

    if not str(normalized.get("wingman_response", "")).strip():
        for key in ("advice", "response", "message", "reply"):
            if normalized.get(key):
                normalized["wingman_response"] = str(normalized[key])
                break

    if not str(normalized.get("energy_read", "")).strip():
        normalized["energy_read"] = "Stay calm and match the situation before reacting."

    messages = normalized.get("suggested_messages")
    if isinstance(messages, str):
        messages = [messages]
    if not isinstance(messages, list):
        messages = []

    cleaned = [str(m).strip() for m in messages if m and str(m).strip()]
    if not cleaned and normalized.get("suggested_message"):
        cleaned = [str(normalized["suggested_message"]).strip()]
    cleaned = [m for m in cleaned if len(m) > 1]
    if not cleaned:
        cleaned = ["if she replies later, just keep it normal and don't over explain"]

    normalized["suggested_messages"] = cleaned[:3]
    normalized.setdefault("mode", "reply_suggestion")
    normalized.setdefault("safety_flag", False)
    normalized.setdefault("confidence", 0.75)

    return normalized
