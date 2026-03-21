import extract_lines  # <- troque pelo nome do seu arquivo .py


def test_main_filters_and_writes(tmp_path, monkeypatch):
    # Setup diretório fake
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()

    file1 = lists_dir / "a.txt"
    file1.write_text("google.com\nmicrosoft.com\nbing.com\n")

    file2 = lists_dir / "b.txt"
    file2.write_text("windows.net\nlinux.org\n")

    output_file = lists_dir / "microsoft.txt"

    # Patch constantes
    monkeypatch.setattr(extract_lines, "LISTS_DIR", str(lists_dir))
    monkeypatch.setattr(extract_lines, "OUTPUT_FILE", str(output_file))

    result = extract_lines.main()

    # Verifica conteúdo
    assert "microsoft.com" in result
    assert "bing.com" in result
    assert "windows.net" in result
    assert "google.com" not in result
    assert "linux.org" not in result

    # Verifica arquivo gerado
    written = output_file.read_text().splitlines()
    assert sorted(result) == written


def test_main_ignores_directories(tmp_path, monkeypatch):
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()

    # cria subdiretório
    (lists_dir / "subdir").mkdir()

    file1 = lists_dir / "a.txt"
    file1.write_text("microsoft.com\n")

    output_file = lists_dir / "microsoft.txt"

    monkeypatch.setattr(extract_lines, "LISTS_DIR", str(lists_dir))
    monkeypatch.setattr(extract_lines, "OUTPUT_FILE", str(output_file))

    result = extract_lines.main()

    assert "microsoft.com" in result


def test_main_skips_output_file(tmp_path, monkeypatch):
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()

    # arquivo destino já existente
    output_file = lists_dir / "microsoft.txt"
    output_file.write_text("bing.com\n")

    file1 = lists_dir / "a.txt"
    file1.write_text("microsoft.com\n")

    monkeypatch.setattr(extract_lines, "LISTS_DIR", str(lists_dir))
    monkeypatch.setattr(extract_lines, "OUTPUT_FILE", str(output_file))
    monkeypatch.setattr(extract_lines, "LIST_DESTINATION", "microsoft.txt")

    result = extract_lines.main()

    assert "microsoft.com" in result


def test_run_and_report_prints(tmp_path, monkeypatch, capsys):
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()

    file1 = lists_dir / "a.txt"
    file1.write_text("microsoft.com\n")

    output_file = lists_dir / "microsoft.txt"

    monkeypatch.setattr(extract_lines, "LISTS_DIR", str(lists_dir))
    monkeypatch.setattr(extract_lines, "OUTPUT_FILE", str(output_file))

    extract_lines.run_and_report()

    captured = capsys.readouterr()

    assert "lines containing" in captured.out
    assert "microsoft" in captured.out


def test__run_main_for_coverage_executes(monkeypatch):
    called = {"ran": False}

    def fake_run():
        called["ran"] = True

    monkeypatch.setattr(extract_lines, "run_and_report", fake_run)

    # Simula execução como script
    monkeypatch.setattr(extract_lines, "__name__", "__main__")

    extract_lines._run_main_for_coverage()

    assert called["ran"] is True


def test__run_main_for_coverage_noop(monkeypatch):
    called = {"ran": False}

    def fake_run():
        called["ran"] = True

    monkeypatch.setattr(extract_lines, "run_and_report", fake_run)

    # Simula import normal
    monkeypatch.setattr(extract_lines, "__name__", "not_main")

    extract_lines._run_main_for_coverage()

    assert called["ran"] is False
