import logging

import podcastindex
import pytest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

@pytest.mark.asyncio
async def test_search_found():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    query_str = "This American Life"
    results = await index.search(query_str)
    found = False

    for feed in results["feeds"]:
        title = feed["title"]
        if query_str == title:
            # Found a matching feed
            found = True
            break

    assert found, "Count not find podcast that should be in the feed: {}".format(query_str)


@pytest.mark.asyncio
async def test_search_clean():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    query_str = "Sex"
    results_dirty = await index.search(query_str, clean=False)
    results_clean = await index.search(query_str, clean=True)

    assert len(results_clean["feeds"]) < len(results_dirty["feeds"])
