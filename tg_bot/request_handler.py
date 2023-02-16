import requests
class RequestHandler():
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()
    
    async def test(self):
        res = self.session.get(self.url)
        return res.json()["1"]