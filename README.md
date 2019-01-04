[![Build Status](https://travis-ci.com/rfechtner/webflowpy.svg?branch=master)](https://travis-ci.com/rfechtner/webflowpy) [![PyPi Version](https://img.shields.io/pypi/v/Webflowpy.svg)](https://pypi.org/project/Webflowpy)

# Webflow CMS API Client

## Disclamer 

This python port of the official [Webflow CMS API Client](https://github.com/webflow/js-webflow-api) (for JS) is not 
maintained by or associated with Webflow.

## Requirements

* Python3 (recommended >= 3.6)
* See requirements.txt

## Installation

Install the package via PyPi:

```shell
$ pip install webflowpy
```

## Usage

```python
from webflowpy.Webflow import Webflow


# Initialize the API
webflow_api = Webflow();

# Fetch a site
webflow_api.site(site_id='580e63e98c9a982ac9b8b741')
```

The `Webflow` constructor takes several options to initialize the API client:

* `token` - the API token **(can also be set via conf.ini - see settings.py)**

All of the API methods are documented in the [API documentation](https://developers.webflow.com).

## Contributing

Contributions are welcome - feel free to open an issue or pull request.

## License

The MIT license - see `LICENSE`.

## Changelog

###### Jan 28th 2019
* Bug Fix

###### Dec 28th 2018

* Initial release 
