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

def test_webflow_items_limit_10_offset_1():
    webflow = Webflow()

    resp = webflow.items(os.getenv('COLLECTION_ID'), limit=5, offset=1)

    assert resp['items'][0]['name'] == 'Fugiat Amet'
    assert int(resp['count']) == 5

def test_webflow_items_all():
    webflow = Webflow()

    resp = webflow.items(os.getenv('COLLECTION_ID'), all = True)

    assert int(resp['count']) > 10

def test_webflow_get_single_item():
    webflow = Webflow()

    # Fetch an item
    resp = webflow.item(os.getenv('COLLECTION_ID'), os.getenv('ITEM_ID'))
    assert int(resp['count']) == 1

def test_webflow_create_update_remove_item():
    webflow = Webflow()

    # Create new live item
    new_item = {
        'name': 'webflowpy-test',
        'slug': 'webflowpy-test',
        '_archived': False,
        '_draft': False
    }

    resp = webflow.createItem(os.getenv('COLLECTION_ID'), new_item, live=True)
    new_item_id = resp['_id']

    assert resp['name'] == new_item['name']

    # Update live item
    update_item = {
        'name': 'webflowpy-test-update',
        'slug': 'webflowpy-test',
        '_archived': False,
        '_draft': False
    }

    resp = webflow.updateItem(os.getenv('COLLECTION_ID'), new_item_id, update_item, live=True)
    new_item_id = resp['_id']
    assert resp['name'] == 'webflowpy-test-update'

    # Delete item
    resp = webflow.removeItem(os.getenv('COLLECTION_ID'), new_item_id)
    assert resp['deleted'] == 1

def test_webflow_publish():
    webflow = Webflow()
    domain_data = { "domains": ["webflowpy-tester.webflow.io"] }

    resp = webflow.publishSite(os.getenv('SITE_ID'), domain_names=domain_data)
    assert resp['queued']