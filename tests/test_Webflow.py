from webflowpy.Webflow import Webflow

def test_webflow_config():
    webflow = Webflow()

    assert webflow.token == 'd9d9faf535a13927a412f968f6e11e465beb44511824c4e48090ef68b3ac36fa'
    assert webflow.version == '1.0.0'

def test_webflow_info():
    webflow = Webflow()

    resp = webflow.info()

    assert resp['status'] == 'confirmed'

def test_webflow_sites():
    webflow = Webflow()

    resp = webflow.site('5c2601f89a1575861286a249')

    assert resp['shortName'] == 'webflowpy-tester'

def test_webflow_collection():
    webflow = Webflow()

    resp = webflow.collection('5c26497f4fdbbae398c05031')

    assert resp['slug'] == 'tests'

def test_webflow_items_limit_10_offset_2():
    webflow = Webflow()

    resp = webflow.items('5c26497f4fdbbae398c05031', limit=10, offset=2)

    assert resp['items'][0]['name'] == 'Sint Error'

def test_webflow_items_all():
    webflow = Webflow()

    resp = webflow.items('5c26497f4fdbbae398c05031', all = True)

    assert int(resp['count']) == 22