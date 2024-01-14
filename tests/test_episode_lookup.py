import logging

import aiohttp
import pytest

import podcastindex

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

feedUrl = "https://lexfridman.com/feed/podcast/"
feedId = 745287
itunesId = 1434243584
badItunesId = "abcdefg1234"

@pytest.mark.asyncio
async def test_episode_lookup_by_feedid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    # Test basic episode retrieval
    results = await index.episodesByFeedId(feedId)
    assert len(results["items"]) > 0, "No episodes found when looking up episodes by feed ID."
    assert (
        results["items"][0]["feedItunesId"] == itunesId
    ), "Episodes found do not belong to the feed ID used in the query"

    # Test with since
    most_recent_ep_timestamp = results["items"][0]["datePublished"]
    since_timestamp = most_recent_ep_timestamp - 1

    results = await index.episodesByFeedId(feedId, since=since_timestamp)
    assert (
        len(results["items"]) > 0
    ), "We should get back at least one episode when looking for episodes since right before the most recent episode."

    for episode in results["items"]:
        assert (
            episode["datePublished"] >= since_timestamp
        ), "Looking for episodes since right before the most recent episode is not correct."


@pytest.mark.asyncio
async def test_episode_lookup_by_feedurl():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.episodesByFeedUrl(feedUrl)
    assert len(results["items"]) > 0, "No episodes found when looking up episodes by feed URL."
    assert (
        results["items"][0]["feedItunesId"] == itunesId
    ), "Episodes found do not belong to the feed URL used in the query"


@pytest.mark.asyncio
async def test_episode_lookup_by_itunesid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.episodesByItunesId(itunesId)
    assert len(results["items"]) > 0, "No episodes found when looking up episodes by Itunes ID."
    assert (
        results["items"][0]["feedItunesId"] == itunesId
    ), "Episodes found do not belong to the Itunes ID used in the query"


@pytest.mark.asyncio
async def test_erroneous_episode_lookup_by_itunesid():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    with pytest.raises(aiohttp.ClientResponseError):
        await index.episodesByItunesId(badItunesId)


@pytest.mark.asyncio
async def test_episode_lookup_by_id():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = await index.episodesByItunesId(itunesId)
    latest_episode_id = results["items"][0]["id"]

    results = await index.episodeById(latest_episode_id)
    assert results["episode"]["id"] == latest_episode_id, "Episode fetched by ID should match ID used in query"
