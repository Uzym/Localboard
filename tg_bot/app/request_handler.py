import aiohttp
import json
import os


class RequestHandler():
    def __init__(self, url):
        self.url = url
        self.session = aiohttp.ClientSession()

    async def my_offers(self, chat_id):
        async with self.session.get(self.url + "/offers/get/my/" + str(chat_id)) as res:
            result = await res.json()
            if res.status == 200:
                return result
            else:
                return {"ans": 0}
    
    async def get_offer(self, offer_id):
        async with self.session.get(self.url + "/offers/get/" + str(offer_id)) as res:
            result = await res.json()
            if res.status == 200:
                return result
            else:
                return {"ans": 0}

    async def new_offer(self, chat_id):
        data = {
            'chat_id': chat_id
        }
        async with self.session.post(self.url + "/offers/add/", json=data) as res:
            result = await res.json()
            if res.status == 200:
                return {"ans": 1, "offer": result}
            else:
                return {"ans": 0}

    async def add_title_offer(self, offer_id, data):
        data = {'offer_id': offer_id, 'title': data}
        async with self.session.post(self.url + "/offers/add/title/", json=data) as res:
            if res.status == 200:
                return {"ans": 1}
            else:
                return {"ans": 0}
    async def add_cost_offer(self, offer_id, data):
        data = {'offer_id': offer_id, 'cost': data}
        async with self.session.post(self.url + "/offers/add/cost/", json=data) as res:
            if res.status == 200:
                return {"ans": 1}
            else:
                return {"ans": 0}
    async def add_desc_offer(self, offer_id, data):
        data = {'offer_id': offer_id, 'desc': data}
        async with self.session.post(self.url + "/offers/add/desc/", json=data) as res:
            if res.status == 200:
                return {"ans": 1}
            else:
                return {"ans": 0}
    async def publish_offer(self, offer_id):
        data = {'offer_id': offer_id, 'hidden': False}
        async with self.session.post(self.url + "/offers/add/hidden/", json=data) as res:
            if res.status == 200:
                return {"ans": 1}
            else:
                return {"ans": 0}
    async def hidden_offer(self, offer_id):
        data = {'offer_id': offer_id, 'hidden': True}
        async with self.session.post(self.url + "/offers/add/hidden/", json=data) as res:
            if res.status == 200:
                return {"ans": 1}
            else:
                return {"ans": 0} 


    async def test(self):
        async with self.session.get(self.url) as res:
            result = await res.json()
            return result["1"]

rh = RequestHandler(os.environ.get("apidemon_url"))
