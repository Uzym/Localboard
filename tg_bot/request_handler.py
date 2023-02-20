import aiohttp
import json


class RequestHandler():
    def __init__(self, url):
        self.url = url
        self.session = aiohttp.ClientSession()

    async def new_offer(self, chat_id):
        data = {
            'chat_id': chat_id
        }
        async with self.session.post(self.url + "/offers/add/", json=data) as res:
            result = await res.json()
            if res.status == 200:
                return {
                    "ans": 1,
                    "offer": result
                }
            else:
                return {
                    "ans": 0
                }

    async def add_title_offer(self, offer_id, data):
        data = {
            'title': data
        }
        async with self.session.post(self.url + "/offers/add/title/", json=data) as res:
            result = await res.json()
            if res.status == 200:
                return {
                    "ans": 1
                }
            else:
                return {
                    "ans": 0
                }


    async def test(self):
        async with self.session.get(self.url) as res:
            result = await res.json()
            return result["1"]
