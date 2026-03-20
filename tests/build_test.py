import os
import runpy
import sys

sys.path.insert(0, os.path.abspath("src"))

import build


def test_get_filenames_without_extension_lists_only_files(tmp_path):
    (tmp_path / "one.txt").write_text("x", encoding="utf-8")
    (tmp_path / "two.list").write_text("x", encoding="utf-8")
    (tmp_path / "folder").mkdir()

    result = build.get_filenames_without_extension(str(tmp_path))

    assert set(result) == {"one", "two"}


def test_delete_file_removes_existing_and_ignores_missing(tmp_path):
    target = tmp_path / "to_delete.txt"
    target.write_text("x", encoding="utf-8")

    build.delete_file(str(target))
    assert not target.exists()

    build.delete_file(str(target))
    assert not target.exists()


def test_selected_lists_filters_and_fallback(monkeypatch):
    monkeypatch.setattr(build, "ADLISTS", ["a", "b", "c"])
    monkeypatch.setattr(build, "ADLISTS_SET", {"a", "b", "c"})

    assert build.selected_lists(["a", "x"]) == ["a"]
    assert build.selected_lists(["x", "y"]) == ["a", "b", "c"]


def test_filter_condition():
    assert build.filter_condition("0.0.0.0 ads.example") is True
    assert build.filter_condition("127.0.0.1 ads.example") is False


def test_load_filtered_lines_filters_by_prefix(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()
    (lists_dir / "test.txt").write_text(
        "0.0.0.0 valid.example\n127.0.0.1 ignored.example\n0.0.0.0 other.example\n",
        encoding="utf-8",
    )

    lines = build.load_filtered_lines("test")
    assert lines == {"0.0.0.0 valid.example", "0.0.0.0 other.example"}


def test_process_combination_writes_sorted_union(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "out").mkdir()
    monkeypatch.setattr(build, "OUTPUT_DIR", "out")

    lines_by_list = {
        "a": {"0.0.0.0 z.example", "0.0.0.0 a.example"},
        "b": {"0.0.0.0 b.example", "0.0.0.0 a.example"},
    }

    build.process_combination(("a", "b"), lines_by_list)

    output = (tmp_path / "out" / "a+b.txt").read_text(encoding="utf-8")
    assert output == "0.0.0.0 a.example\n0.0.0.0 b.example\n0.0.0.0 z.example\n"


def test_main_generates_all_combinations(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()
    (lists_dir / "a.txt").write_text("0.0.0.0 a.example\n", encoding="utf-8")
    (lists_dir / "b.txt").write_text("0.0.0.0 b.example\n", encoding="utf-8")

    monkeypatch.setattr(build, "ADLISTS", ["a", "b"])
    monkeypatch.setattr(build, "ADLISTS_SET", {"a", "b"})
    monkeypatch.setattr(build, "OUTPUT_DIR", "out")
    monkeypatch.setenv("LISTS", "a,b")

    build.main()

    out_dir = tmp_path / "out"
    assert (out_dir / "a.txt").exists()
    assert (out_dir / "b.txt").exists()
    assert (out_dir / "a+b.txt").exists()

    assert (out_dir / "a+b.txt").read_text(encoding="utf-8") == "0.0.0.0 a.example\n0.0.0.0 b.example\n"


def test_build_dunder_main_executes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    lists_dir = tmp_path / "lists"
    lists_dir.mkdir()
    (lists_dir / "a.txt").write_text("0.0.0.0 a.example\n", encoding="utf-8")
    monkeypatch.setenv("LISTS", "a")

    runpy.run_module("build", run_name="__main__")

    assert (tmp_path / "out" / "a.txt").exists()
