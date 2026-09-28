import os
import runpy
import sys

sys.path.insert(0, os.path.abspath("src"))
import readme_list
from settings import PROJECT_REPO


def test_get_filenames_without_extension(tmp_path):
    (tmp_path / "one.txt").write_text("x", encoding="utf-8")
    (tmp_path / "two.list").write_text("x", encoding="utf-8")
    (tmp_path / "folder").mkdir()
    result = readme_list.get_filenames_without_extension(str(tmp_path))
    assert set(result) == {"one", "two"}


def test_main_prints_a_row_per_list_with_descriptive_link_text(monkeypatch, capsys):
    monkeypatch.setattr(readme_list, "get_filenames_without_extension", lambda directory: ["phishing", "ads"])

    readme_list.main()

    out = capsys.readouterr().out
    assert f"| ads | [ads.txt](https://raw.githubusercontent.com/{PROJECT_REPO}/master/lists/ads.txt) |" in out
    assert f"| phishing | [phishing.txt](https://raw.githubusercontent.com/{PROJECT_REPO}/master/lists/phishing.txt) |" in out
    # sorted regardless of the order get_filenames_without_extension returned them in
    assert out.index("| ads |") < out.index("| phishing |")


def test_main_entrypoint(capsys):
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/readme_list.py"))
    runpy.run_path(src_path, run_name="__main__")

    out = capsys.readouterr().out
    assert "| List  | Description" in out
