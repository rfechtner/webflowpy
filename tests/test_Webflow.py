import os
from webflowpy.Webflow import Webflow

def test_webflow_config():
    webflow = Webflow()

    # Set by environment variable 'WEBFLOW_API_KEY'
    assert webflow.token != ''

    assert webflow.version == '1.0.0'

def test_webflow_info():
    webflow = Webflow()

    resp = webflow.info()

    assert resp['status'] == 'confirmed'

def test_webflow_sites():
    webflow = Webflow()

    resp = webflow.site(os.getenv('SITE_ID'))

    assert resp['shortName'] == 'webflowpy-tester'

def test_webflow_collection():
    webflow = Webflow()

    resp = webflow.collection(os.getenv('COLLECTION_ID'))

    assert resp['slug'] == 'tests'

def test_webflow_items_limit_10_offset_2():
    webflow = Webflow()

    resp = webflow.items(os.getenv('COLLECTION_ID'), limit=10, offset=2)

    assert resp['items'][0]['name'] == 'Fugiat Amet'

def test_webflow_items_all():
    webflow = Webflow()

    resp = webflow.items(os.getenv('COLLECTION_ID'), all = True)

    assert int(resp['count']) == 20