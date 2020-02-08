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

def test_webflow_items_get_create_update_remove():
    webflow = Webflow()

    # Fetch an item
    resp = webflow.item(os.getenv('COLLECTION_ID'), os.getenv('ITEM_ID'))
    item_name = resp['items'][0]['name']

    assert int(resp['count']) == 1
    assert item_name == "Id"

    # Create new live item
    new_name = item_name + '-test'
    new_item = {
        'name': new_name,
        'slug': 'test_create',
        '_archived': False,
        '_draft': False
    }
    resp = webflow.createItem(os.getenv('COLLECTION_ID'), new_item, live=True)
    new_item_id = resp['_id']
    assert resp['name'] == new_name

    # Update live item
    update_item = {
        'name': new_name + "-update",
        'slug': 'test_create',
        '_archived': False,
        '_draft': False
    }

    resp = webflow.updateItem(os.getenv('COLLECTION_ID'), new_item_id, update_item, live = True)

    assert resp['name'] == new_name + "-update"

    # Delete item
    resp = webflow.removeItem(os.getenv('COLLECTION_ID'), new_item_id)

    assert resp['deleted'] == 1
