import aiohttp
import json

class RequestHandler():
    def __init__(self, url):
        self.url = url
        self.session = aiohttp.ClientSession()

    async def new_offer(self, chat_id):
        data = {
            "chat_id": chat_id
        }
        async with self.session.post(self.url + "/offers/add/", data=data) as res:
            result = await res.text()
            return result

    async def test(self):
        async with self.session.get(self.url) as res:
            result = await res.json()
            return result["1"]
