[![Build Status](https://travis-ci.com/SarvagyaVaish/python-podcastindex.svg?branch=main)](https://travis-ci.com/SarvagyaVaish/python-podcastindex)
[![codecov](https://codecov.io/gh/SarvagyaVaish/python-podcastindex/branch/main/graph/badge.svg?token=H154DI9JUR)](https://codecov.io/gh/SarvagyaVaish/python-podcastindex)

# python-podcastindex

A python wrapper for the Podcast Index API (podcastindex.org)

## Installation

(coming soon)

## Usage

### Init the podcast index
```python
import podcastindex

config = {
    "api_key": "YOUR API KEY HERE",
    "api_secret": "YOUR API SECRET HERE"
}

index = podcast_index.init(config)
```

### Search

```python
result = index.search("This American Life")
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

## Contributing

(coming soon)
