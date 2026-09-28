import common


def test_get_filenames_without_extension_lists_only_files(tmp_path):
    (tmp_path / "a.txt").write_text("x")
    (tmp_path / "b.txt").write_text("y")
    (tmp_path / "subdir").mkdir()

    result = common.get_filenames_without_extension(str(tmp_path))

    assert sorted(result) == ["a", "b"]


def test_delete_file_removes_existing_and_ignores_missing(tmp_path):
    target = tmp_path / "file.txt"
    target.write_text("data")

    common.delete_file(str(target))
    assert not target.exists()

    common.delete_file(str(target))  # missing file: no error


def test_line_has_prefix():
    assert common.line_has_prefix("0.0.0.0 example.com", "0.0.0.0") is True
    assert common.line_has_prefix("example.com", "0.0.0.0") is False


def test_filter_selected_lists_filters_and_falls_back():
    all_lists = ["a", "b", "c"]

    assert common.filter_selected_lists(["a", "x"], all_lists) == ["a"]
    assert common.filter_selected_lists(["x", "y"], all_lists) == all_lists
    assert common.filter_selected_lists(["a"], all_lists, all_lists_set={"a", "b", "c"}) == ["a"]


def test_configure_logging_is_safe_to_call_repeatedly():
    common.configure_logging()
    common.configure_logging()  # idempotent: must not raise or duplicate handlers
