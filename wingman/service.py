from wingman.client import WingmanClient
from wingman.config import Settings, get_settings
from wingman.schema import WingmanResult


class WingmanService:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client = WingmanClient(self.settings)

    def is_ready(self) -> bool:
        return self._client.is_configured()

    def advise(
        self,
        user_input: str,
        *,
        relationship_stage: str | None = None,
        user_emotion: str | None = None,
    ) -> WingmanResult:
        return self._client.generate(
            user_input,
            relationship_stage=relationship_stage,
            user_emotion=user_emotion,
            cache_hit=True,
        )
