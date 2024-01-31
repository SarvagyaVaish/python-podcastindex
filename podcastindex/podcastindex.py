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

        # Timeout used when making requests
        self.timeout = 5

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

    def _make_request_get_result_helper(self, url, payload):
        """
        Helper method DRY up the code. It performs the request and returns the result.

        Returns:
            [type]: [description]
        """
        # Perform request
        headers = self._create_headers()
        result = requests.post(url, headers=headers,
                               data=payload, timeout=self.timeout)
        result.raise_for_status()

        # Parse the result as a dict
        result_dict = json.loads(result.text)
        return result_dict

    def search(self, query, clean=False):
        """
        Returns all of the feeds that match the search terms in the title, author or owner of the feed.

        Args:
            query (str): Query string
            clean (bool): Return only non-explicit feeds

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/search/byterm"

        # Setup payload
        payload = {"q": query}
        if clean:
            payload["clean"] = 1

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def podcastByFeedUrl(self, feedUrl):
        """
        Lookup a podcast by feedUrl.

        Args:
            feedUrl (string): The feed's url.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/podcasts/byfeedurl"

        # Setup payload
        payload = {"url": feedUrl}

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def podcastByFeedId(self, feedId):
        """
        Lookup a podcast by feedId.

        Args:
            feedId (string or integer): Podcast index internal ID.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/podcasts/byfeedid"

        # Setup payload
        payload = {"id": feedId}

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def podcastByItunesId(self, itunesId):
        """
        Lookup a podcast by itunesId.

        Args:
            itunesId (string or integer): Itunes ID for the feed.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/podcasts/byitunesid"

        # Setup payload
        payload = {"id": itunesId}

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def episodesByFeedUrl(self, feedUrl, since=None, max_results=10, fulltext=False):
        """
        Lookup episodes by feedUrl, returned in reverse chronological order.

        Args:
            feedUrl (string or integer): The feed's url.
            since (integer): Unix timestamp, or a negative integer that represents a number of seconds prior to right
                             now. The search will start from that time and only return feeds updated since then.
            max_results (integer): Maximum number of results to return. Default: 10
            fulltext (bool): Return full text in the text fields. Default: False

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/episodes/byfeedurl"

        # Setup payload
        payload = {"url": feedUrl, "max": max_results}
        if since:
            payload["since"] = since
        if fulltext:
            payload["fulltext"] = True

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def episodesByFeedId(
        self, feedId, since=None, max_results=10, fulltext=False, enclosure=None
    ):
        """
        Lookup episodes by feedId, returned in reverse chronological order.

        Args:
            feedId (string or integer): Podcast index internal ID.
            since (integer): Unix timestamp, or a negative integer that represents a number of seconds prior to right
                             now. The search will start from that time and only return feeds updated since then.
            max_results (integer): Maximum number of results to return. Default: 10
            fulltext (bool): Return full text in the text fields. Default: False
            enclosure (string): The URL for the episode enclosure to get the information for.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/episodes/byfeedid"

        # Setup payload
        payload = {"id": feedId, "max": max_results}
        if since:
            payload["since"] = since
        if fulltext:
            payload["fulltext"] = True
        if enclosure:
            payload["enclosure"] = enclosure

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def episodesByItunesId(
        self, itunesId, since=None, max_results=10, fulltext=False, enclosure=None
    ):
        """
        Lookup episodes by itunesId, returned in reverse chronological order.

        Args:
            itunesId (string or integer): Itunes ID for the feed.
            since (integer): Unix timestamp, or a negative integer that represents a number of seconds prior to right
                now. The search will start from that time and only return feeds updated since then.
            max_results (integer): Maximum number of results to return. Default: 10
            fulltext (bool): Return full text in the text fields. Default: False
            enclosure (string): The URL for the episode enclosure to get the information for.


        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/episodes/byitunesid"

        # Setup payload
        payload = {
            "id": itunesId,
            "max": max_results,
            "fulltext": True,
        }
        if since:
            payload["since"] = since
        if fulltext:
            payload["fulltext"] = True
        if enclosure:
            payload["enclosure"] = enclosure

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def episodeById(self, id, fulltext=False):
        """
        Lookup episode by id internal to podcast index.

        Args:
            id (string or integer): Episode ID.
            fulltext (bool): Return full text in the text fields. Default: False

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/episodes/byid"

        # Setup payload
        payload = {"id": id}
        if fulltext:
            payload["fulltext"] = True

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def episodeByGuid(
        self, guid, feedurl=None, feedid=None, podcastguid=None, fulltext=False
    ):
        """
        Lookup episode by guid.

        Args:
            guid (string): Episode GUID.
            feedurl (string): The feed's url.
            feedid (string or integer): Podcast index internal ID.
            podcastguid (string): The GUID of the podcast to search within.
            fulltext (bool): Return full text in the text fields. Default: False

            *guid and at least one of feedurl or feedid must be specified.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        if not guid:
            raise ValueError("guid must not be None or empty")
        if not (feedurl or feedid or podcastguid):
            raise ValueError(
                "At least one of feedurl or feedid or podcastguid must not be None or empty"
            )

        # Setup request
        url = self.base_url + "/episodes/byguid"

        # Setup payload
        payload = {"guid": guid}
        if feedurl:
            payload["feedurl"] = feedurl
        if feedid:
            payload["feedid"] = feedid
        if podcastguid:
            payload["podcastguid"] = podcastguid
        if fulltext:
            payload["fulltext"] = True

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def episodesByPerson(self, query, clean=False, fulltext=False):
        """
        Returns all of the episodes where the specified person is mentioned.

        Args:
            query (str): Query string
            clean (bool): Return only non-explicit feeds
            fulltext (bool): Return full text in the text fields. Default: False

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/search/byperson"

        # Setup payload
        payload = {"q": query}
        if clean:
            payload["clean"] = 1
        if fulltext:
            payload["fulltext"] = True

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def recentEpisodes(
        self, max=None, excluding=None, before_episode_id=None, fulltext=False
    ):
        """
        Returns the most recent [max] number of episodes globally across the whole index, in reverse chronological
        order.

        Args:
            max (int, optional): Maximum number of results to return.
            excluding ([type], optional): Any item containing this string in the title or url will be discarded from
                the result set.
            before_episode_id (int, optional): Get recent episodes before this episode id, allowing you to walk back
                through the episode history sequentially.
            fulltext (bool): Return full text in the text fields. Default: False

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/recent/episodes"

        # Setup payload
        payload = {}
        if max:
            payload["max"] = max
        if excluding:
            payload["excludeString"] = excluding
        if before_episode_id:
            payload["before"] = before_episode_id
        if fulltext:
            payload["fulltext"] = True

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def recentFeeds(
        self, max=40, since=None, lang=None, categories=None, not_categories=None
    ):
        """
        Returns the most recent [max] feeds, in reverse chronological order.

        Args:
            max (int, optional): Maximum number of results to return. Default: 40
            since (int): Return items since the specified time. Can be a unix epoch timestamp or a negative integer
                that represents a number of seconds prior to right now
            lang ([string], optional): Specifying a language code will return podcasts only in that language.
            categories ([string or int], optional): A list of categories used to limit which podcasts will be included
                in results. Category names and IDs are both supported.
            not_categories ([string or int], optional): A list of categories used to limit exclude certain podcasts
                from results. Category names and IDs are both supported.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/recent/feeds"

        # Setup payload
        payload = {}
        if max:
            payload["max"] = max
        if since:
            payload["since"] = since
        if lang:
            payload["lang"] = ",".join(str(i) for i in lang)
        if categories:
            payload["cat"] = ",".join(str(i) for i in categories)
        if not_categories:
            payload["notcat"] = ",".join(str(i) for i in not_categories)

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def newFeeds(self, max=40, since=None, feed_id=None, desc=None):
        """
        Returns every new feed added to the index over the past 24 hours in reverse chronological order.

        Args:
            max (int, optional): Maximum number of results to return. Default: 40
            since (int): Return items since the specified time. Can be a unix epoch timestamp or a negative integer
                that represents a number of seconds prior to right now
            feed_id (string or int): The PodcastIndex Feed ID to start from (or go to if desc specified).
                If since parameter also specified, value of since is ignored.
            desc (bool): If true, return results in descending order. Only applicable when using feedid parameter.
                Default: False

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/recent/feeds"

        # Setup payload
        payload = {}
        if max:
            payload["max"] = max
        if since:
            payload["since"] = since
        if feed_id:
            payload["feedid"] = feed_id
        if desc:
            payload["desc"] = desc

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def trendingPodcasts(
        self, max=10, since=None, lang=None, categories=None, not_categories=None
    ):
        """
        Returns the podcasts in the index that are trending.

        Args:
            max (int): Maximum number of results to return. Default: 10
            since (int): Return items since the specified time. Can be a unix epoch timestamp or a negative integer
                that represents a number of seconds prior to right now
            lang ([string], optional): Specifying a language code will return podcasts only in that language.
            categories ([string or int], optional): A list of categories used to limit which podcasts will be included
                in results. Category names and IDs are both supported.
            not_categories ([string or int], optional): A list of categories used to limit exclude certain podcasts
                from results. Category names and IDs are both supported.
        """
        # Setup request
        url = self.base_url + "/podcasts/trending"

        # Setup payload
        payload = {}
        if max:
            payload["max"] = max
        if since:
            payload["since"] = since
        if lang:
            payload["lang"] = ",".join(str(i) for i in lang)
        if categories:
            payload["cat"] = ",".join(str(i) for i in categories)
        if not_categories:
            payload["notcat"] = ",".join(str(i) for i in not_categories)

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def addByItunesId(self, itunesId):
        """
        Request a podcast be added to the index based on itunesId.

        Args:
            itunesId (string or integer): Itunes ID for the feed.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/add/byitunesid"

        # Setup payload
        payload = {
            "id": itunesId,
            "pretty": 1,
        }

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)

    def pubNotifyUpdate(self, id):
        """
        Request a podcast be updated.

        Args:
            id (string or integer): ID of the podcast to update.

        Raises:
            requests.exceptions.HTTPError: When the status code is not OK.
            requests.exceptions.ReadTimeout: When the request times out.

        Returns:
            Dict: API response
        """
        # Setup request
        url = self.base_url + "/hub/pubnotify"

        # Setup payload
        payload = {
            "id": id,
            "pretty": 1,
        }

        # Call Api for result
        return self._make_request_get_result_helper(url, payload)
