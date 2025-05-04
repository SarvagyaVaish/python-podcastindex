import logging

import podcastindex

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

def test_random_episodes():
    config = podcastindex.get_config_from_env()
    index = podcastindex.init(config)

    # Basic test
    results = index.randomEpisodes(max=1)
    assert len(results["episodes"]) == 1, "Expected exactly one episode."

    # Test that changing the `max` parameter impacts the number of episodes returned
    results = index.randomEpisodes(max=3)
    assert len(results["episodes"]) == 3, "Expected exactly three episodes."
