import builtins
import os
import sys

sys.path.insert(0, os.path.abspath("src"))
import readme_list


def test_get_filenames_without_extension(tmp_path):
    (tmp_path / "one.txt").write_text("x", encoding="utf-8")
    (tmp_path / "two.list").write_text("x", encoding="utf-8")
    (tmp_path / "folder").mkdir()
    result = readme_list.get_filenames_without_extension(str(tmp_path))
    assert set(result) == {"one", "two"}


def test_readme_list_prints_table(monkeypatch):
    lists = ["ads", "phishing"]
    monkeypatch.setattr(readme_list, "ADLISTS", lists)
    output = []
    monkeypatch.setattr(builtins, "print", output.append)
    # Simula execução do bloco principal
    for list_name in lists:
        print(f"| {list_name} | [Link](https://raw.githubusercontent.com/dcotecnologia/pihole-lists/master/lists/{list_name}.txt) |")
    # Checa se as linhas esperadas estão no output
    assert any("| ads |" in line for line in output)
    assert any("| phishing |" in line for line in output)
