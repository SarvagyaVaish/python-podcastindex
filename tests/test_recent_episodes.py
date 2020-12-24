import logging
import time

import podcastindex

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

feedUrl = "http://feed.thisamericanlife.org/talpodcast"
feedId = 522613
itunesId = 201671138


def _log_results(context, results):
    logger.info("Episode results from {}".format(context))
    for episode in results["items"]:
        logger.info(
            "Episode Id: {} \t Date: {}, {} \t ".format(
                episode["id"], episode["datePublished"], episode["datePublishedPretty"]
            )
        )


# # Uncomment once the API is fixed.
# def test_recent_episodes():
#     config = podcastindex.get_config_from_env()
#     index = podcastindex.init(config)

#     results = index.recentEpisodes(max=10)
#     _log_results("test_recent_episodes", results)

#     # Last episode should be within the last day
#     last_episode_timestamp = results["items"][0]["datePublished"]
#     assert time.time() - last_episode_timestamp < 24 * 3600

#     # Episodes are ordered in reverse chronological order
#     for i in range(1, len(results["items"])):
#         more_recent_timestamp = results["items"][i - 1]["datePublished"]
#         next_item_timestamp = results["items"][i]["datePublished"]
#         assert (
#             more_recent_timestamp >= next_item_timestamp
#         ), "Recent episodes should be returned in reverse chronological order"


def test_recent_episodes_max():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    results = index.recentEpisodes(max=15)
    assert len(results["items"]) == 15, "By default we expect to get back 10 results"


# # Uncomment once the API is fixed.
# def test_recent_episodes_before_id():
#     config = podcastindex.get_config_from_env()
#     index = podcastindex.init(config)

#     results = index.recentEpisodes(max=10)
#     _log_results("test_recent_episodes_before_id", results)
#     prev_oldest_id = results["items"][-1]["id"]
#     prev_oldest_timestamp = results["items"][-1]["datePublished"]

#     results = index.recentEpisodes(max=1, before_episode_id=prev_oldest_id)
#     _log_results("test_recent_episodes_before_id", results)
#     for episode in results["items"]:
#         episode_timestamp = episode["datePublished"]
#         assert episode_timestamp >= prev_oldest_timestamp, "Using before episode id, we should get older results"
