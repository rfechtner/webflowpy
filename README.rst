| |Build Status| |PyPI| |PyPi Stats|  

.. |Build Status| image:: https://travis-ci.org/rfechtner/webflowpy.svg?branch=master
   :target: https://travis-ci.org/rfechtner/webflowpy
.. |PyPI| image:: https://img.shields.io/pypi/v/webflowpy.svg
    :target: https://pypi.org/project/webflowpy
.. |PyPi Stats| image:: https://img.shields.io/pypi/dm/webflowpy.svg
   :target: https://pypistats.org/packages/webflowpy

Webflow CMS API Client
======================

Disclamer
---------

This python port of the official `Webflow CMS API Client <https://github.com/webflow/js-webflow-api>`_ (for JS) is not 
maintained by or associated with Webflow.

Requirements
------------

- Python3 (recommended >= 3.6)
- See requirements.txt

Installation
------------

Install the package via PyPi:

.. code::
 $ pip install webflowpy


Usage
-----


.. code:: python

    from webflowpy.Webflow import Webflow

    # Initialize the API
    webflow_api = Webflow()

    # Fetch a site
    webflow_api.site(site_id='XXX')


  
The `Webflow` constructor takes several options to initialize the API client:

- `token` - the API token **(can also be set via conf.ini - see settings.py)**

All of the API methods are documented in the `API documentation <https://developers.webflow.com>`_ .

Contributing
------------

Contributions are welcome - feel free to open an issue or pull request.

License
-------

The MIT license - see `LICENSE`.

Changelog
---------

Jan 28th 2019
_____________
* Bug Fix

Dec 28th 2018
_____________
* Initial release 
