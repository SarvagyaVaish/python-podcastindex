import logging
import time

import podcastindex
import pytest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


def _log_results(context, results):
    logger.ingo("Podcast results from {}".format(context))
    for feed in results["feeds"]:
        logger.info(
            "Podcast Id: {} \t Title: {} \t Newest item publish time: {} \t Categories: {}".format(
                feed["id"], feed["title"], feed["newestItemPublishTime"], feed["categories"])
        )


@pytest.mark.asyncio
async def test_trending_podcasts_max():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.trendingPodcasts(max=15)
    assert len(results["feeds"]
               ) == 15, "By default we expect to get back 10 results"


@pytest.mark.asyncio
async def test_trending_podcasts_since():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.trendingPodcasts(since=-(24 * 3600))
    for feed in results["feeds"]:
        last_updated = feed["newestItemPublishTime"]
        assert time.time() - last_updated < 24 * 3600


@pytest.mark.asyncio
async def test_trending_podcasts_lang():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.trendingPodcasts(lang=["es"])
    for feed in results["feeds"]:
        assert feed["language"] == "es"


@pytest.mark.asyncio
async def test_trending_podcasts_categories():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)
    categories = ["News", "Comedy"]

    results = await index.trendingPodcasts(categories=categories)
    for feed in results["feeds"]:
        assert categories[0] in feed["categories"].values(
        ) or categories[1] in feed["categories"].values()


@pytest.mark.asyncio
async def test_trending_podcasts_not_categories():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)
    categories = ["News", "Comedy"]

    results = await index.trendingPodcasts(not_categories=categories)
    for feed in results["feeds"]:
        for id in feed["categories"]:
            assert not feed["categories"][id] in categories
