import asyncio
import aiohttp
from aiohttp import web
from dummy_connector import Connector


class Server:
    def __init__(self):
        self.app = web.Application()
        self.app.add_routes([web.get('/ws', self.websocket_handler)])
        self.app.add_routes([web.static('/', './')])

        self.app.on_startup.append(self._start_background_tasks)
        self.app.on_cleanup.append(self._cleanup_background_tasks)
        self.websockets = []

    def run(self):
        print('Running app')
        web.run_app(self.app)
        print('Donning app')

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        self.websockets.append(ws)
        # Read inbound messages from websocket
        async for msg in ws:
            # We don't actually care about inbound messages,
            # so we drop them on the floor unless they're errors
            if msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        print('websocket connection closed')

        # Remove the newly-closed socket from the server's list of sockets
        self.websockets = [socket for socket in self.websockets if socket != ws]
        return ws

    async def _handle_new_data(self, new_data):
        for ws in self.websockets:
            await ws.send_str(str(new_data))

    async def _start_background_tasks(self, app):
        c = Connector(self._handle_new_data)
        app['connector_task'] = asyncio.create_task(c.start_exchanges())

    async def _cleanup_background_tasks(self, app):
        app['connector_task'].cancel()
        await app['connector_task']
