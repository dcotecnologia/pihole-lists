import pytest

from app import lists_repo


@pytest.fixture(autouse=True)
def lists_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(lists_repo, "LISTS_DIR", tmp_path)
    return tmp_path


def write_list(lists_dir, name, domains):
    (lists_dir / f"{name}.txt").write_text("".join(f"0.0.0.0 {d}\n" for d in domains), encoding="utf-8")


def test_list_lists_empty_dir(lists_dir):
    assert lists_repo.list_lists() == []


def test_list_lists_counts_prefixed_lines_only(lists_dir):
    (lists_dir / "a.txt").write_text("0.0.0.0 x.example\n# comment\n0.0.0.0 y.example\n", encoding="utf-8")

    result = lists_repo.list_lists()

    assert result == [{"name": "a", "item_count": 2}]


def test_create_list_creates_empty_file(lists_dir):
    lists_repo.create_list("newlist")

    assert (lists_dir / "newlist.txt").read_text(encoding="utf-8") == ""


def test_create_list_rejects_invalid_name(lists_dir):
    with pytest.raises(lists_repo.InvalidNameError):
        lists_repo.create_list("../etc")


def test_create_list_rejects_duplicate(lists_dir):
    lists_repo.create_list("dup")
    with pytest.raises(lists_repo.ListAlreadyExistsError):
        lists_repo.create_list("dup")


def test_delete_list_removes_file(lists_dir):
    lists_repo.create_list("todelete")
    lists_repo.delete_list("todelete")

    assert not (lists_dir / "todelete.txt").exists()


def test_delete_list_missing_raises(lists_dir):
    with pytest.raises(lists_repo.ListNotFoundError):
        lists_repo.delete_list("missing")


def test_get_items_paginates_and_filters(lists_dir):
    write_list(lists_dir, "big", ["foo.test", "foobar.test", "quux.test"])

    page = lists_repo.get_items("big", query="foo", page=1, page_size=1)
    assert page == {"items": ["foo.test"], "total": 2, "page": 1, "page_size": 1}

    page2 = lists_repo.get_items("big", query="foo", page=2, page_size=1)
    assert page2["items"] == ["foobar.test"]


def test_get_items_missing_list_raises(lists_dir):
    with pytest.raises(lists_repo.ListNotFoundError):
        lists_repo.get_items("missing")


def test_add_item_appends_new_domain(lists_dir):
    lists_repo.create_list("adds")

    added = lists_repo.add_item("adds", "new.example")

    assert added is True
    assert lists_repo.get_items("adds")["items"] == ["new.example"]


def test_add_item_is_idempotent(lists_dir):
    lists_repo.create_list("adds")
    lists_repo.add_item("adds", "dup.example")

    added_again = lists_repo.add_item("adds", "dup.example")

    assert added_again is False
    assert lists_repo.get_items("adds")["total"] == 1


def test_add_item_rejects_invalid_domain(lists_dir):
    lists_repo.create_list("adds")
    with pytest.raises(lists_repo.InvalidNameError):
        lists_repo.add_item("adds", "not a domain")


def test_add_item_missing_list_raises(lists_dir):
    with pytest.raises(lists_repo.ListNotFoundError):
        lists_repo.add_item("missing", "x.example")


def test_remove_item_deletes_matching_line(lists_dir):
    write_list(lists_dir, "rm", ["a.example", "b.example"])

    removed = lists_repo.remove_item("rm", "a.example")

    assert removed is True
    assert lists_repo.get_items("rm")["items"] == ["b.example"]


def test_remove_item_missing_domain_returns_false(lists_dir):
    write_list(lists_dir, "rm", ["a.example"])

    assert lists_repo.remove_item("rm", "missing.example") is False


def test_remove_item_missing_list_raises(lists_dir):
    with pytest.raises(lists_repo.ListNotFoundError):
        lists_repo.remove_item("missing", "x.example")
