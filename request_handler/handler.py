from aiohttp import web
import json
from db import DB

db = DB()
handlers = web.RouteTableDef()

@handlers.get('/location_list')
async def offer_get(request: web.Request) -> web.Response:

    result = await db.location_list()
    
    return web.json_response(
        result, text=None, body=None, status=200, reason=None,
        headers=None, content_type='application/json', dumps=json.dumps
    )

@handlers.get('/offer_list')
async def offer_get(request: web.Request) -> web.Response:
    location_id = request.rel_url.query['location_id']

    result = await db.offer_list(location_id)
    
    return web.json_response(
        result, text=None, body=None, status=200, reason=None,
        headers=None, content_type='application/json', dumps=json.dumps
    )

@handlers.get('/offer_open')
async def offer_open(request) -> web.Response:
    offer_id = request.rel_url.query['offer_id']
    
    result = await db.offer_open(offer_id)

    return web.json_response(
        result, text=None, body=None, status=200, reason=None,
        headers=None, content_type='application/json', dumps=json.dumps
    )

@handlers.get('/offer_new')
async def offer_new(request) -> web.Response:
    title = request.rel_url.query['title']
    cost = request.rel_url.query['cost']
    tag = request.rel_url.query['tag']
    desc = request.rel_url.query['desc']
    user_id = request.rel_url.query['user_id']
    hidden = request.rel_url.query['hidden']
    location_id = request.rel_url.query['location_id']
    
    result = await db.offer_new(title, cost, tag, desc, user_id, hidden, location_id)

    return web.json_response(
        result, text=None, body=None, status=200, reason=None,
        headers=None, content_type='application/json', dumps=json.dumps
    )

# offer_change
# offer_delete
# request_new
# request_delete
# location_new
