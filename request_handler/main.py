from aiohttp import web
from handler import handlers
import logging

app = web.Application()
app.add_routes(handlers)

if __name__ == '__main__':
    logging.info("Start request_handler...")
    web.run_app(app)
