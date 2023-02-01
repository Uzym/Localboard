import asyncio
import psycopg2

class DB:
    def __init__(self) -> None:
        pass
    
    async def location_list(self) -> list:
        result = [
            {
                "Location_ID": 0,
                "Title": "Global"
            },
            {
                "Location_ID": 1,
                "Title": "Russia"
            },
            {
                "Location_ID": 2,
                "Title": "Moscow"
            }
        ]
        return result
    
    async def offer_list(self, location_id) -> list:
        result = [
            {
                "test": "test"
            }
        ]
        return result
        
    async def offer_open(self, offer_id) -> list:
        result = [
            {
                "offer_id": offer_id,
                "title": "Test",
                "Cost": "100",
                "tag": "test",
                "desc": "test test test",
                "user_id": "0",
                "user_name": "TestName",
            }
        ]
        return result
    
    async def offer_new(self, title, cost, tag, desc, user_id, hidden, location_id) -> list:
        result = [
            {
                "Ok": True
            }
        ]
