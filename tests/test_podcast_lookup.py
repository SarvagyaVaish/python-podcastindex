import logging

import podcastindex

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

podcastTitle = "This American Life"
feedUrl = "http://feed.thisamericanlife.org/talpodcast"
feedId = 522613
itunesId = 201671138


def test_podcast_lookup_by_feedurl():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = index.podcastByFeedUrl(feedUrl)
    assert results["feed"]["title"] == podcastTitle, "Did not find the right podcast when doing lookup by URL"


def test_podcast_lookup_by_byfeedid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = index.podcastByFeedId(feedId)
    assert results["feed"]["title"] == podcastTitle, "Did not find the right podcast when doing lookup by Feed ID"


def test_podcast_lookup_by_byitunesid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = index.podcastByItunesId(itunesId)
    assert results["feed"]["title"] == podcastTitle, "Did not find the right podcast when doing lookup by Itunes ID"
