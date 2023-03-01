import aiohttp
import json
import os

from app.config import config


class RequestHandler():
    def __init__(self, url):
        self.url = url
        self.session = aiohttp.ClientSession(loop=config.loop)

    async def get_user_chat_id(self, user_id: int):
        async with self.session.get(self.url + "/users/get/chat_id/" + str(user_id)) as res:
            result = await res.json()
            if res.status == 200:
                return result
            else:
                return {"ans": 0}
    
    async def get_list_offers(self, chat_id: str, use_chat_id: bool, use_hidden: bool, list_start: int, list_end: int):
        data = {
            "use_chat_id": use_chat_id,
            "chat_id": chat_id,
            "use_hidden": use_hidden,
            "list_start": list_start,
            "list_end": list_end
        }
        async with self.session.post(self.url + "/offers/get/list/", json=data) as res:
            result = await res.json()
            if res.status == 200:
                return result
            else:
                return {"ans": 0}

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
                return result
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
    async def add_quantity_offer(self, offer_id, data):
        data = {'offer_id': offer_id, 'quantity': data}
        async with self.session.post(self.url + "/offers/add/quantity/", json=data) as res:
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
    
    async def delete_offer(self, offer_id):
        async with self.session.delete(self.url + "/offers/delete/" + str(offer_id)) as res:
            result = await res.json()
            if res.status == 200:
                return result
            else:
                return {"ans": 0}

    async def upload_photo(self, offer_id, file):
        data = {'photo': file, "offer_id": offer_id}
        async with self.session.post(self.url + "/offers/photo/add/", json=data) as res:
            if res.status == 200:
                return {"ans": 1}
            else:
                return {"ans": 0}
        

rh = RequestHandler(os.environ.get("apidemon_url"))
