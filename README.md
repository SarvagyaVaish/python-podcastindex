# python-podcastindex

A python wrapper for the Podcast Index API (podcastindex.org)

## Installation

```
pip install python-podcastindex
```

## Usage

1. [ Init the podcast index ](#init)
1. [ Search ](#search)
1. [ Podcasts ](#podcasts)
1. [ Episodes of a podcast ](#episode_of_a_podcast)
1. [ Episode by ID ](#episodes_by_id)
1. [ Recent episodes ](#recent_episodes)


<a name="init"></a>
### Init the podcast index
```python
import podcastindex

config = {
    "api_key": "YOUR API KEY HERE",
    "api_secret": "YOUR API SECRET HERE"
}

index = podcastindex.init(config)
```

<a name="search"></a>
### Search

```python
result = index.search("This American Life")
result = index.search("This American Life", clean=True)
```

<details>
  <summary>Click to see sample result!</summary>

  ```javascript
    {
        "status": "true",
        "feeds": [
            {
                "id": 522613,
                "title": "This American Life",
                "url": "http://feed.thisamericanlife.org/talpodcast",
                "originalUrl": "http://feed.thisamericanlife.org/talpodcast",
                "link": "https://www.thisamericanlife.org",
                "description": "This American Life is a weekly public ...",
                "author": "This American Life",
                "ownerName": "",
                "image": "https://files.thisamericanlife.org/sites/all/themes/thislife/img/tal-name-1400x1400.png",
                "artwork": "https://files.thisamericanlife.org/sites/all/themes/thislife/img/tal-name-1400x1400.png",
                "lastUpdateTime": 1607323495,
                "lastCrawlTime": 1607632436,
                "lastParseTime": 1607323495,
                "lastGoodHttpStatusTime": 1607632436,
                "lastHttpStatus": 200,
                "contentType": "text/xml; charset=UTF-8",
                "itunesId": 201671138,
                "generator": null,
                "language": "en",
                "type": 0,
                "dead": 0,
                "crawlErrors": 0,
                "parseErrors": 0,
                "categories": {
                    "77": "Society",
                    "78": "Culture",
                    "1": "Arts",
                    "55": "News",
                    "59": "Politics"
                },
                "locked": 0,
                "imageUrlHash": 1124696616
            },
            ...
        ],
        "count": 8,
        "query": "This American Life",
        "description": "Found matching feeds."
    }
  ```
</details>

<a name="podcasts"></a>
### Podcasts

```python
results = index.podcastByFeedId(522613)
results = index.podcastByFeedUrl("http://feed.thisamericanlife.org/talpodcast")
results = index.podcastByItunesId(201671138)
```

<details>
  <summary>Click to see sample result!</summary>

  ```javascript
    {
        "status": "true",
        "query": {
            "id": "201671138"
        },
        "feed": {
            "id": 522613,
            "title": "This American Life",
            "url": "http://feed.thisamericanlife.org/talpodcast",
            "originalUrl": "http://feed.thisamericanlife.org/talpodcast",
            "link": "https://www.thisamericanlife.org",
            "description": "This American Life is a weekly public radio show, heard by 2.2 million people on more than 500 stations. Another 2.5 million people download the weekly podcast. It is hosted by Ira Glass, produced in collaboration with Chicago Public Media, delivered to stations by PRX The Public Radio Exchange, and has won all of the major broadcasting awards.",
            "author": "This American Life",
            "ownerName": "",
            "image": "https://files.thisamericanlife.org/sites/all/themes/thislife/img/tal-name-1400x1400.png",
            "artwork": "https://files.thisamericanlife.org/sites/all/themes/thislife/img/tal-name-1400x1400.png",
            "lastUpdateTime": 1607927945,
            "lastCrawlTime": 1608430718,
            "lastParseTime": 1608376393,
            "lastGoodHttpStatusTime": 1608430718,
            "lastHttpStatus": 200,
            "contentType": "text/xml; charset=UTF-8",
            "itunesId": 201671138,
            "generator": null,
            "language": "en",
            "type": 0,
            "dead": 0,
            "crawlErrors": 0,
            "parseErrors": 0,
            "locked": 0
        },
        "description": "Found matching items."
    }
  ```
</details>

<a name="episode_of_a_podcast"></a>
### Episodes of a podcast

```python
results = index.episodesByFeedId(522613)
results = index.episodesByFeedUrl("http://feed.thisamericanlife.org/talpodcast")
results = index.episodesByItunesId(201671138)

results = index.episodesByFeedId(522613, since=-525600)  # in the last year
results = index.episodesByFeedId(522613, since=1577836800)  # Jan 1st 2020
```

<details>
  <summary>Click to see sample result!</summary>

  ```javascript
    {
        "status": "true",
        "items": [
            {
                "id": 1270106072,
                "title": "726: Twenty-Five",
                "link": "http://feed.thisamericanlife.org/~r/talpodcast/~3/p41tfsPlK00/twenty-five",
                "description": "To commemorate our show\u2019s 25th year, we have a program about people who were born the year our show went on\u00a0the\u00a0air.",
                "guid": "44678 at https://www.thisamericanlife.org",
                "datePublished": 1607900400,
                "datePublishedPretty": "December 13, 2020 5:00pm",
                "dateCrawled": 1607927945,
                "enclosureUrl": "https://www.podtrac.com/pts/redirect.mp3/podcast.thisamericanlife.org/podcast/726.mp3",
                "enclosureType": "audio/mpeg",
                "enclosureLength": 0,
                "duration": 3561,
                "explicit": 0,
                "episode": null,
                "episodeType": null,
                "season": 0,
                "image": "",
                "feedItunesId": 201671138,
                "feedImage": "https://files.thisamericanlife.org/sites/all/themes/thislife/img/tal-name-1400x1400.png",
                "feedId": 522613,
                "feedLanguage": "en",
                "chaptersUrl": null,
                "transcriptUrl": null
            },
            ...
        ],
        "count": 28,
        "query": "201671138",
        "description": "Found matching items."
    }
  ```
</details>

<a name="episodes_by_id"></a>
### Episode by ID

```python
results = index.episodeById(1270106072)
```

<details>
  <summary>Click to see sample result!</summary>

  ```javascript
    {
        "status": "true",
        "id": "1270106072",
        "episode": {
            "id": 1270106072,
            "title": "726: Twenty-Five",
            "link": "http://feed.thisamericanlife.org/~r/talpodcast/~3/p41tfsPlK00/twenty-five",
            "description": "To commemorate our show\u2019s 25th year, we have a program about people who were born the year our show went on\u00a0the\u00a0air.",
            "guid": "44678 at https://www.thisamericanlife.org",
            "datePublished": 1607900400,
            "datePublishedPretty": "December 13, 2020 5:00pm",
            "dateCrawled": 1607927945,
            "enclosureUrl": "https://www.podtrac.com/pts/redirect.mp3/podcast.thisamericanlife.org/podcast/726.mp3",
            "enclosureType": "audio/mpeg",
            "enclosureLength": 0,
            "duration": 3561,
            "explicit": 0,
            "episode": null,
            "episodeType": null,
            "season": 0,
            "image": "",
            "feedItunesId": 201671138,
            "feedImage": "https://files.thisamericanlife.org/sites/all/themes/thislife/img/tal-name-1400x1400.png",
            "feedId": 522613,
            "feedTitle": "This American Life",
            "feedLanguage": "en",
            "chaptersUrl": null,
            "transcriptUrl": null
        },
        "description": "Found matching item."
    }
  ```
</details>

<a name="recent_episodes"></a>
### Recent episodes

```python
results = index.recentEpisodes(max=5, excluding="trump", before_episode_id=1270106072)
```

<details>
  <summary>Click to see sample result!</summary>

  ```javascript
    {
        "status": "true",
        "items": [
            {
                "id": 1269804903,
                "title": "How epidemics and pandemics have changed history",
                "link": "http://www.abc.net.au/radionational/programs/rearvision/how-epidemics-and-pandemics-have-changed-history/12851986",
                "description": "Human history is usually understood through wars, economic changes, technological development or great leaders. What\u2019s frequently overlooked is the role of infectious disease epidemics and pandemics. But as the COVID-19 virus has reminded us, disease can change us in ways we could never imagine.",
                "guid": "http://www.abc.net.au/radionational/programs/rearvision/how-epidemics-and-pandemics-have-changed-history/12851986",
                "datePublished": 1608426300,
                "datePublishedPretty": "December 19, 2020 7:05pm",
                "dateCrawled": 1607923316,
                "enclosureUrl": "http://mpegmedia.abc.net.au/rn/podcast/2020/12/rvn_20201220.mp3",
                "enclosureType": "audio/mp3",
                "enclosureLength": 27955968,
                "explicit": 0,
                "episode": null,
                "episodeType": null,
                "season": 0,
                "image": "",
                "feedItunesId": 135114451,
                "feedImage": "http://www.abc.net.au/cm/rimage/9860262-1x1-thumbnail.jpg?v=2",
                "feedId": 990878,
                "feedTitle": "Rear Vision",
                "feedLanguage": "en-AU"
            },
            ...
        ],
        "count": 5,
        "max": "5",
        "description": "Found matching items."
    }
  ```
</details>

## Running the tests

- Export the api key and secret

```
export PODCAST_INDEX_API_KEY="7B3U8VVP87QWSZUFXJRE"
export PODCAST_INDEX_API_SECRET="4QwK83LA7RttCDdms9MnCn3HMYqGPG6CDEvnkL2w"
```

- Run the tests

```
coverage run -m pytest --log-cli-level=INFO
```

## Contributing

- Fork the repo
- Add your awesome code
- Submit a pull request
- Ensure all existing tests pass
- Bonus: include tests for your awesome new feature

## Updating the pip package

This is mostly for myself since I have to lookup these commands every time ;)

1. Update version number in setup.py
2. Run the following commands
```
rm -rf build
rm -rf dist
python3 -m pip install --upgrade build
python3 -m build
```
3. Check that there is a .tar.gz and .whl file in the dist folder
4. Upload the new version
```
python3 -m pip install --upgrade twine
twine upload dist/*
```

## Support

I am passionate about podcasting and work on this in my spare time. Hit me up and we can grab a virtual coffee together.

<a href="https://www.buymeacoffee.com/survyv" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
