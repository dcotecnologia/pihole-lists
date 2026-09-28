import settings


def test_env_selected_lists_uses_default_when_env_unset(monkeypatch):
    monkeypatch.delenv(settings.LISTS_ENV_VAR, raising=False)

    assert settings.env_selected_lists(["a", "b"]) == ["a", "b"]


def test_env_selected_lists_parses_and_strips_env_value(monkeypatch):
    monkeypatch.setenv(settings.LISTS_ENV_VAR, " a , b ,,c")

    assert settings.env_selected_lists(["default"]) == ["a", "b", "c"]
