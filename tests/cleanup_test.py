import io
import os
import runpy
import sys

import dns.exception
import dns.resolver

sys.path.insert(0, os.path.abspath("src"))

import cleanup


def test_get_filenames_without_extension_lists_only_files(tmp_path):
    (tmp_path / "one.txt").write_text("x", encoding="utf-8")
    (tmp_path / "two.list").write_text("x", encoding="utf-8")
    (tmp_path / "folder").mkdir()

    result = cleanup.get_filenames_without_extension(str(tmp_path))
    assert set(result) == {"one", "two"}


def test_delete_file_removes_existing_and_ignores_missing(tmp_path):
    target = tmp_path / "to_delete.txt"
    target.write_text("x", encoding="utf-8")

    cleanup.delete_file(str(target))
    assert not target.exists()

    cleanup.delete_file(str(target))
    assert not target.exists()


def test_check_line_starts_with_and_integrity_message(tmp_path, capsys):
    assert cleanup.check_line_starts_with("abc", "a") is True
    assert cleanup.check_line_starts_with("abc", "z") is False

    import logging
    from io import StringIO

    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # Remove all handlers to avoid duplicate logs
    for h in logger.handlers[:]:
        logger.removeHandler(h)
    logger.addHandler(handler)
    try:
        existing = tmp_path / "exists.txt"
        existing.write_text("x", encoding="utf-8")
        cleanup.integrity_message(str(existing))
        handler.flush()
        log_contents = log_stream.getvalue()
        assert "compiled successfully" in log_contents

        log_stream.truncate(0)
        log_stream.seek(0)

        missing = tmp_path / "missing.txt"
        cleanup.integrity_message(str(missing))
        handler.flush()
        log_contents = log_stream.getvalue()
        assert "couldn't be compiled" in log_contents
    finally:
        logger.removeHandler(handler)
        handler.close()


def test_selected_lists_filters_and_fallback(monkeypatch):
    monkeypatch.setattr(cleanup, "ADLISTS", ["a", "b"])
    monkeypatch.setattr(cleanup, "ADLISTS_SET", {"a", "b"})

    assert cleanup.selected_lists(["a", "x"]) == ["a"]
    assert cleanup.selected_lists(["x"]) == ["a", "b"]


def test_extract_domain_from_line_returns_normalized():
    domain, normalized = cleanup.extract_domain_from_line("0.0.0.0 example.com   # comment", "0.0.0.0")
    assert domain == "example.com"
    assert normalized == "0.0.0.0 example.com"


def test_extract_domain_from_line_invalid_prefix_or_format():
    assert cleanup.extract_domain_from_line("127.0.0.1 example.com", "0.0.0.0") == (None, None)
    assert cleanup.extract_domain_from_line("0.0.0.0", "0.0.0.0") == (None, None)


def test_get_max_dns_workers_env_override_and_invalid(monkeypatch):
    monkeypatch.delenv("DNS_WORKERS", raising=False)
    fallback = min(32, (os.cpu_count() or 1) * 5)
    assert cleanup.get_max_dns_workers() == fallback

    monkeypatch.setenv("DNS_WORKERS", "7")
    assert cleanup.get_max_dns_workers() == 7

    monkeypatch.setenv("DNS_WORKERS", "invalid")
    assert cleanup.get_max_dns_workers() == fallback


def test_is_valid_domain_or_ip_ipv4(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", False)
    assert cleanup.is_valid_domain_or_ip("1.1.1.1") is True


def test_is_valid_domain_or_ip_ipv6(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", False)
    assert cleanup.is_valid_domain_or_ip("2001:4860:4860::8888") is True


def test_is_valid_domain_or_ip_invalid_domain(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", False)
    assert cleanup.is_valid_domain_or_ip("not a domain") is False


def test_is_valid_domain_or_ip_dns_success(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", True)

    def _ok(*_args, **_kwargs):
        return ["ok"]

    monkeypatch.setattr(cleanup.dns.resolver, "resolve", _ok)
    assert cleanup.is_valid_domain_or_ip("example.com") is True


def test_is_valid_domain_or_ip_dns_failure(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", True)

    def _raise_timeout(*_args, **_kwargs):
        raise dns.exception.Timeout

    monkeypatch.setattr(cleanup.dns.resolver, "resolve", _raise_timeout)
    assert cleanup.is_valid_domain_or_ip("example.com") is False


def test_is_valid_domain_or_ip_nonameservers(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", True)

    def _raise_nonameservers(*_args, **_kwargs):
        raise dns.resolver.NoNameservers

    monkeypatch.setattr(cleanup.dns.resolver, "resolve", _raise_nonameservers)
    assert cleanup.is_valid_domain_or_ip("example.com") is False


def test_is_valid_domain_or_ip_outer_dns_exception(monkeypatch):
    cleanup.is_valid_domain_or_ip.cache_clear()
    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", False)

    def _raise_timeout(*_args, **_kwargs):
        raise dns.exception.Timeout

    monkeypatch.setattr(cleanup.validators.ip_address, "ipv4", _raise_timeout)
    assert cleanup.is_valid_domain_or_ip("example.com") is False


def test_process_file_filters_invalid_and_logs(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    input_file.write_text(
        "0.0.0.0 valid.example\n0.0.0.0 invalid.example\n0.0.0.0 valid.example  # duplicate\n127.0.0.1 ignored.example\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", False)

    def fake_validator(domain):
        return domain == "valid.example"

    monkeypatch.setattr(cleanup, "is_valid_domain_or_ip", fake_validator)

    log_buffer = io.StringIO()
    result = cleanup.process_file(str(input_file), "0.0.0.0", log_buffer)

    assert result == ["0.0.0.0 valid.example"]
    assert "invalid.example - refused by validators/dns" in log_buffer.getvalue()


def test_process_file_handles_invalid_entry_without_domain(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    input_file.write_text("0.0.0.0\n", encoding="utf-8")

    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", False)
    log_buffer = io.StringIO()

    result = cleanup.process_file(str(input_file), "0.0.0.0", log_buffer)
    assert result == []


def test_process_file_dns_threaded_branch(tmp_path, monkeypatch):
    input_file = tmp_path / "input.txt"
    input_file.write_text(
        "0.0.0.0 valid.example\n0.0.0.0 invalid.example\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(cleanup, "CHECK_DOMAIN_DNS", True)
    monkeypatch.setattr(cleanup, "get_max_dns_workers", lambda: 2)

    class DummyFuture:
        def __init__(self, value):
            self._value = value

        def result(self):
            return self._value

    class DummyExecutor:
        def __init__(self, max_workers):
            self.max_workers = max_workers

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def submit(self, fn, domain):
            return DummyFuture(fn(domain))

    monkeypatch.setattr(cleanup, "ThreadPoolExecutor", DummyExecutor)
    monkeypatch.setattr(cleanup, "as_completed", lambda futures: list(futures))
    monkeypatch.setattr(cleanup, "is_valid_domain_or_ip", lambda d: d == "valid.example")

    log_buffer = io.StringIO()
    result = cleanup.process_file(str(input_file), "0.0.0.0", log_buffer)

    assert result == ["0.0.0.0 valid.example"]
    assert "invalid.example - refused by validators/dns" in log_buffer.getvalue()


def test_cleanup_main_rewrites_selected_lists(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()
    (lists_dir / "a.txt").write_text("0.0.0.0 old.example\n", encoding="utf-8")

    monkeypatch.setattr(cleanup, "ADLISTS", ["a"])
    monkeypatch.setattr(cleanup, "ADLISTS_SET", {"a"})
    monkeypatch.setenv("LISTS", "a")
    monkeypatch.setattr(cleanup, "process_file", lambda *_args, **_kwargs: ["0.0.0.0 rewritten.example"])

    cleanup.main()

    content = (lists_dir / "a.txt").read_text(encoding="utf-8")
    assert content == "0.0.0.0 rewritten.example\n"


def test_cleanup_dunder_main_executes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()
    (lists_dir / "a.txt").write_text("0.0.0.0 1.1.1.1\n", encoding="utf-8")
    monkeypatch.setenv("LISTS", "a")
    monkeypatch.setenv("CHECK_DOMAIN_DNS", "0")
    (tmp_path / ".log-config.yml").write_text(
        "version: 1\nhandlers:\n  console:\n    class: logging.StreamHandler\n    level: INFO\nroot:\n  level: INFO\n  handlers: [console]\n",
        encoding="utf-8",
    )

    runpy.run_module("cleanup", run_name="__main__")

    assert (lists_dir / "a.txt").exists()
    assert (tmp_path / "log.txt").exists()
