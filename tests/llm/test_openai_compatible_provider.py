import pytest

from src.core.config import Settings
from src.llm.openai_compatible_provider import OpenAICompatibleProvider


def make_settings(**overrides) -> Settings:
    base = {
        "DATABASE_URL": "postgresql+asyncpg://u:p@localhost:5432/db",
        "LLM_API_KEY": "test-key",
    }
    base.update(overrides)
    return Settings(**base)


class TestOpenAICompatibleProvider:
    def test_construction_without_key_does_not_raise(self):
        # http/condition workflows must not require an LLM key
        provider = OpenAICompatibleProvider(make_settings(LLM_API_KEY=""))
        assert provider._client is None

    def test_get_client_without_key_raises(self):
        provider = OpenAICompatibleProvider(make_settings(LLM_API_KEY=""))
        with pytest.raises(ValueError, match="LLM_API_KEY"):
            provider._get_client()

    def test_get_client_with_key_builds_and_caches(self):
        provider = OpenAICompatibleProvider(make_settings(LLM_API_KEY="k"))
        client = provider._get_client()
        assert client is not None
        assert provider._get_client() is client  # закеширован
