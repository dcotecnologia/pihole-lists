import importlib.util
import os
import runpy
import sys
import types

src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/import.py"))
spec = importlib.util.spec_from_file_location("import_mod", src_path)
import_mod = importlib.util.module_from_spec(spec)
sys.modules["import_mod"] = import_mod
spec.loader.exec_module(import_mod)


def load_import_mod(alias="import_mod_dynamic"):
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/import.py"))
    spec = importlib.util.spec_from_file_location(alias, src_path)
    assert spec is not None, "spec is None, cannot import src/import.py"
    module = importlib.util.module_from_spec(spec)
    sys.modules[alias] = module
    spec.loader.exec_module(module)
    return module


def test_extract_host_hosts_format():
    assert import_mod.extract_host("0.0.0.0 example.com") == "example.com"
    assert import_mod.extract_host("127.0.0.1 test.com") == "test.com"


def test_extract_host_url_format():
    assert import_mod.extract_host("https://example.com/path") == "example.com"
    assert import_mod.extract_host("http://test.com:8080/") == "test.com"


def test_extract_host_plain_domain():
    assert import_mod.extract_host("plain.com") == "plain.com"
    assert import_mod.extract_host("plain.com:1234") == "plain.com"


def test_extract_host_empty_and_comment():
    assert import_mod.extract_host("") is None
    assert import_mod.extract_host("# comment") is None


def test_import_main_creates_output(tmp_path, monkeypatch):
    import_mod2 = load_import_mod("import_mod2")

    test_source = tmp_path / "source.txt"
    test_source.write_text("0.0.0.0 a.com\nhttps://b.com\nplain.com\n", encoding="utf-8")

    log_calls = {"info": 0, "error": 0}

    def fake_info(*args, **kwargs):
        log_calls["info"] += 1

    def fake_error(*args, **kwargs):
        log_calls["error"] += 1

    monkeypatch.setattr(
        import_mod2,
        "logging",
        types.SimpleNamespace(info=fake_info, error=fake_error),
    )
    monkeypatch.setattr(import_mod2, "SOURCES", {"test": f"file://{test_source}"})
    monkeypatch.setattr(import_mod2, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(
        import_mod2.requests,
        "get",
        lambda url, timeout=10: type(
            "Resp",
            (),
            {"status_code": 200, "text": test_source.read_text(encoding="utf-8")},
        )(),
    )

    out_file = tmp_path / "test_hosts.txt"
    if out_file.exists():
        out_file.unlink()

    import_mod2.main()

    assert out_file.exists()
    content = out_file.read_text(encoding="utf-8")
    assert "0.0.0.0 a.com" in content
    assert "0.0.0.0 b.com" in content
    assert "0.0.0.0 plain.com" in content
    assert log_calls["info"] > 0


def test_import_main_logs_error_on_non_200(tmp_path, monkeypatch):
    import_mod2 = load_import_mod("import_mod3")

    test_source = tmp_path / "source.txt"
    test_source.write_text("0.0.0.0 a.com\n", encoding="utf-8")

    log_calls = {"info": 0, "error": 0}

    def fake_info(*args, **kwargs):
        log_calls["info"] += 1

    def fake_error(*args, **kwargs):
        log_calls["error"] += 1

    monkeypatch.setattr(
        import_mod2,
        "logging",
        types.SimpleNamespace(info=fake_info, error=fake_error),
    )
    monkeypatch.setattr(import_mod2, "SOURCES", {"fail": f"file://{test_source}"})
    monkeypatch.setattr(import_mod2, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(
        import_mod2.requests,
        "get",
        lambda url, timeout=10: type("Resp", (), {"status_code": 404, "text": "not found"})(),
    )

    import_mod2.main()

    assert log_calls["error"] > 0


def test_import_main_logs_error_on_exception(tmp_path, monkeypatch):
    import_mod2 = load_import_mod("import_mod4")

    test_source = tmp_path / "source.txt"
    test_source.write_text("0.0.0.0 a.com\n", encoding="utf-8")

    log_calls = {"info": 0, "error": 0}

    def fake_info(*args, **kwargs):
        log_calls["info"] += 1

    def fake_error(*args, **kwargs):
        log_calls["error"] += 1

    monkeypatch.setattr(
        import_mod2,
        "logging",
        types.SimpleNamespace(info=fake_info, error=fake_error),
    )
    monkeypatch.setattr(import_mod2, "SOURCES", {"error": f"file://{test_source}"})
    monkeypatch.setattr(import_mod2, "OUTPUT_DIR", str(tmp_path))

    def raise_exc(url, timeout=10):
        raise Exception("test error")

    monkeypatch.setattr(import_mod2.requests, "get", raise_exc)

    import_mod2.main()

    assert log_calls["error"] > 0


def test_import_main_logs_info_when_no_new_hosts(tmp_path, monkeypatch):
    import_mod2 = load_import_mod("import_mod5")

    test_source = tmp_path / "source.txt"
    test_source.write_text("0.0.0.0 a.com\nhttps://b.com\nplain.com\n", encoding="utf-8")

    out_file = tmp_path / "test_hosts.txt"
    out_file.write_text(
        "0.0.0.0 a.com\n0.0.0.0 b.com\n0.0.0.0 plain.com\n",
        encoding="utf-8",
    )

    log_calls = {"info": 0, "error": 0}

    def fake_info(*args, **kwargs):
        log_calls["info"] += 1

    def fake_error(*args, **kwargs):
        log_calls["error"] += 1

    monkeypatch.setattr(
        import_mod2,
        "logging",
        types.SimpleNamespace(info=fake_info, error=fake_error),
    )
    monkeypatch.setattr(import_mod2, "SOURCES", {"test": f"file://{test_source}"})
    monkeypatch.setattr(import_mod2, "OUTPUT_DIR", str(tmp_path))
    monkeypatch.setattr(
        import_mod2.requests,
        "get",
        lambda url, timeout=10: type(
            "Resp",
            (),
            {"status_code": 200, "text": test_source.read_text(encoding="utf-8")},
        )(),
    )

    import_mod2.main()

    assert log_calls["info"] > 0
    assert log_calls["error"] == 0


def test_main_entrypoint(tmp_path, monkeypatch):
    test_source = tmp_path / "source.txt"
    test_source.write_text("0.0.0.0 a.com\n", encoding="utf-8")

    monkeypatch.setenv("OUTPUT_DIR", str(tmp_path))

    import sources

    monkeypatch.setattr(sources, "SOURCES", {"test": f"file://{test_source}"})

    import requests

    monkeypatch.setattr(
        requests,
        "get",
        lambda url, timeout=10: type("Resp", (), {"status_code": 200, "text": test_source.read_text(encoding="utf-8")})(),
    )

    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/import.py"))
    runpy.run_path(src_path, run_name="__main__")

    assert (tmp_path / "test_hosts.txt").exists()
