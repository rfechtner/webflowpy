from webflowpy import settings
from webflowpy.WebflowResponse import WebflowResponse
from webflowpy.utils import requests_retry_session
from webflowpy import log as logg

from typing import Optional

DEFAULT_ENDPOINT = 'https://api.webflow.com'
VERSION = '1.0.0'

class Webflow:
    def __init__(
            self,
            token: Optional[str] = None
    ):
        if token:
            self.token = token
        else:
            self.token = settings.token

        self.endpoint = DEFAULT_ENDPOINT
        self.version = VERSION

        self.headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {token}'.format(token = self.token),
            'accept-version': self.version,
            'Content-Type': 'application/json',
        }

    def __query(
            self,
            method: str,
            path: str,
            data: Optional[dict] = {}
    ):
        url = self.endpoint + path

        try:
            response = requests_retry_session().request(
                method, headers=self.headers, url=url, json=data
            )
        except Exception as x:
            logg.error("No valid response after {retries} attempts. Aborting!".format(retries = settings.retries + 1))
            if settings.abort_on_error:
                exit(1)
        else:
            resp_parsed = WebflowResponse(response)
            return resp_parsed.response

    # META

    def info(self):
        return self.__query('GET', '/info')

    # SITES

    def sites(self):
        return self.__query('GET', '/sites')

    def site(self, site_id):
        return self.__query('GET', '/sites/{site_id}'.format(site_id = site_id))

    def publishSite(self, site_id, domain_names):
        """Takes site_id->str and domain_names->list as arguments"""
        domains = {"domains": domain_names}
        return self.__query('POST', '/sites/{site_id}/publish'.format(site_id = site_id), data=domains)

    # DOMAINS

    def domains(self, site_id):
        return self.__query('GET', '/sites/{site_id}/domains'.format(site_id=site_id))

    # COLLECTIONS

    def collections(self, site_id):
        return self.__query('GET', '/sites/{site_id}/collections'.format(site_id=site_id))

    def collection(self, collection_id):
        return self.__query('GET', '/collections/{collection_id}'.format(collection_id=collection_id))

    # ITEMS

    def items(self, collection_id, limit = 100, offset = 0, all = False):
        if all:
            all_items = []
            resp = self.items(collection_id, offset=offset, all=False)
            all_items.extend(resp['items'])

            while(len(all_items) < resp['total']):
                offset += 100
                resp = self.items(collection_id, offset=offset, all=False)
                all_items.extend(resp['items'])

            resp['items'] = all_items
            resp['count'] = len(all_items)

            return resp
        else:
            return self.__query('GET', '/collections/{collection_id}/items?limit={limit}&offset={offset}'.format(
                collection_id=collection_id, limit = limit, offset = offset
            ))

    def item(self, collection_id, item_id):
        return self.__query('GET', '/collections/{collection_id}/items/{item_id}'.format(
            collection_id=collection_id, item_id = item_id
        ))

    def createItem(self, collection_id, item_data, live = False):
        data = {}
        data['fields'] = item_data

        l = '?live=true' if live else ''

        return self.__query('POST', '/collections/{collection_id}/items{live}'.format(
            collection_id=collection_id, live = l
        ), data = data)

    def updateItem(self, collection_id, item_id, item_data, live = False):
        data = {}
        data['fields'] = item_data

        l = '?live=true' if live else ''

        return self.__query('PUT', '/collections/{collection_id}/items/{item_id}{live}'.format(
            collection_id=collection_id, item_id = item_id, live = l
        ), data = data)

    def patchItem(self, collection_id, item_id, item_data, live = False):
        data = {}
        data['fields'] = item_data

        l = '?live=true' if live else ''

        return self.__query('PATCH', '/collections/{collection_id}/items/{item_id}{live}'.format(
            collection_id=collection_id, item_id = item_id, live = l
        ), data=data)

    def removeItem(self, collection_id, item_id):
        return self.__query('DELETE', '/collections/{collection_id}/items/{item_id}'.format(
            collection_id=collection_id, item_id = item_id
        ))

    # ECOMMERCE

    def orders(self, site_id):
        return self.__query('GET', '/sites/{site_id}/orders'.format(site_id=site_id))

    def order(self, site_id, order_id):
        return self.__query('GET', '/sites/{site_id}/order/{order_id}'.format(site_id=site_id, order_id = order_id))

    def updateOrder(self, site_id, order_id, order_data):
        data = {}
        data['fields'] = order_data

        return self.__query(
            'PATCH', '/sites/{site_id}/order/{order_id}'.format(site_id=site_id, order_id=order_id),
            data=data
        )

    def fulfillOrder(self, site_id, order_id):
        return self.__query('POST', '/sites/{site_id}/order/{order_id}/fulfill'.format(
            site_id=site_id, order_id = order_id
        ))

    def unfulfillOrder(self, site_id, order_id):
        return self.__query('POST', '/sites/{site_id}/order/{order_id}/unfulfill'.format(
            site_id=site_id, order_id = order_id
        ))

    def refundOrder(self, site_id, order_id):
        return self.__query('POST', '/sites/{site_id}/order/{order_id}/refund'.format(
            site_id=site_id, order_id = order_id
        ))

    def itemInventory(self, collection_id, item_id):
        return self.__query('GET', '/collections/{collection_id}/items/{item_id}/inventory'.format(
            collection_id=collection_id, item_id=item_id
        ))

    def updateItemInventory(self, collection_id, item_id, inventory_data):
        data = {}
        data['fields'] = inventory_data

        return self.__query('PATCH', '/collections/{collection_id}/items/{item_id}/inventory'.format(
            collection_id=collection_id, item_id=item_id
        ), data=data)
    
    def products(self, site_id):
        return self.__query('GET', '/sites/{site_id}/products'.format(site_id=site_id))

    # WEBHOOKS

    def webhooks(self, site_id):
        return self.__query('GET', '/sites/{site_id}/webhooks'.format(site_id=site_id))

    def webhook(self, site_id, webhook_id):
        return self.__query(
            'GET', '/sites/{site_id}/webhooks/{webhook_id}'.format(site_id=site_id, webhook_id=webhook_id)
        )

    def createWebhook(self, site_id, triggerType, url, filter):
        data = {
            'triggerType': triggerType,
            'url': url,
            'filter': filter
        }

        return self.__query('POST', '/sites/{site_id}/webhooks'.format(site_id=site_id), data=data)

    def removeWebhook(self, site_id, webhook_id):
        return self.__query(
            'DELETE', '/sites/{site_id}/webhooks/{webhook_id}'.format(site_id=site_id, webhook_id=webhook_id)
        )
