import hashlib
import json
import logging
import os
import time

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def init(config):
    """
    Create and return a new PodcastIndex object, initialized using the config.

    Args:
        config (Dict): Dictionary with 'api_key' and 'api_secret' keys.

    Returns:
        PodcastIndex: Initialized PodcastIndex object.
    """
    return PodcastIndex(config)


def get_config_from_env():
    """
    Retrieve the api key and secret from the envoronment.

    Raises:
        RuntimeError: If the key or secret is not found in the environment.

    Returns:
        Dict: config with "api_key" and "api_secret"
    """
    api_key = os.getenv("PODCAST_INDEX_API_KEY")
    if api_key is None:
        error_msg = "Could not find PODCAST_INDEX_API_KEY environment variable"
        raise RuntimeError(error_msg)

    api_secret = os.environ.get("PODCAST_INDEX_API_SECRET")
    if api_secret is None:
        error_msg = "Could not find PODCAST_INDEX_API_SECRET environment variable"
        raise RuntimeError(error_msg)

    config = {"api_key": api_key, "api_secret": api_secret}
    return config


class PodcastIndex:
    def __init__(self, config):
        assert "api_key" in config
        assert "api_secret" in config

        self.api_key = config["api_key"]
        self.api_secret = config["api_secret"]

        self.base_url = "https://api.podcastindex.org/api/1.0"

    def _create_headers(self):
        """
        Hash the current timestamp along with the api key and secret to
        produce the headers for calling the api.

        Returns:
            dict: dictionary of header data
        """
        # we'll need the unix time
        epoch_time = int(time.time())

        # our hash here is the api key + secret + time
        data_to_hash = self.api_key + self.api_secret + str(epoch_time)

        # which is then sha-1'd
        sha_1 = hashlib.sha1(data_to_hash.encode()).hexdigest()

        # now we build our request headers
        headers = {
            "X-Auth-Date": str(epoch_time),
            "X-Auth-Key": self.api_key,
            "Authorization": sha_1,
            "User-Agent": "Voyce",
        }

        return headers

    def search(self, query, clean=False):
        """
        Returns all of the feeds that match the search terms in the title, author or owner of the feed.

        Args:
            query (str): Query string
            clean (bool): Return only non-explicit feeds

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.

        Returns:
            Dict: API response
        """
        # Setup request
        headers = self._create_headers()
        url = self.base_url + "/search/byterm"

        # Setup payload
        payload = {"q": query}
        if clean:
            payload["clean"] = 1

        # Perform request
        result = requests.post(url, headers=headers, data=payload)
        result.raise_for_status()

        # Parse the result as a dict
        result_dict = json.loads(result.text)
        return result_dict
