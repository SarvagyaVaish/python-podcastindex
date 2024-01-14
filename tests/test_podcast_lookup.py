import logging

import podcastindex
import pytest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

podcastTitle = "This American Life"
feedUrl = "http://feed.thisamericanlife.org/talpodcast"
feedId = 522613
itunesId = 201671138


@pytest.mark.asyncio
async def test_podcast_lookup_by_feedurl():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.podcastByFeedUrl(feedUrl)
    assert results["feed"]["title"] == podcastTitle, "Did not find the right podcast when doing lookup by URL"


@pytest.mark.asyncio
async def test_podcast_lookup_by_byfeedid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.podcastByFeedId(feedId)
    assert results["feed"]["title"] == podcastTitle, "Did not find the right podcast when doing lookup by Feed ID"


@pytest.mark.asyncio
async def test_podcast_lookup_by_byitunesid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.podcastByItunesId(itunesId)
    assert results["feed"]["title"] == podcastTitle, "Did not find the right podcast when doing lookup by Itunes ID"
