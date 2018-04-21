from path import Path
import pytest

import mastoback.search


@pytest.fixture
def tmp_path(tmpdir):
    return Path(tmpdir)


def test_search(tmp_path):
    index = mastoback.search.Index(tmp_path)
    toot_one = mastoback.Toot(1, "one", {"tags": ["foo", "bar"]})
    toot_two = mastoback.Toot(2, "two", {"tags": ["spam", "eggs"]})
    index.add_toot(toot_one)
    index.add_toot(toot_two)
    results = index.search_text("one")
    assert results
