import asyncio
import aiohttp
from aiohttp import web
from background_job import SomeBackgroundJob


class Server:
    def __init__(self):
        self.app = web.Application()  # Create the "app" object
        self.app.add_routes([
            web.get('/ws', self.websocket_handler),  # Tells the server how to handle weboscket connection requests
            web.static('/', './'),  # Tells the server how to handle static files
        ])
        self.app.on_startup.append(self._start_background_tasks)  # Create a "task" to start when the server starts
        self.app.on_cleanup.append(self._cleanup_background_tasks)  # Create a "task" to run when the server finishes
        self.websockets = []

    def run(self):
        web.run_app(self.app)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()

        # Tells the client (the webpage) that it is OK to evolve from an HTTP connection to a WebSocket connection
        await ws.prepare(request)

        # Keep track of the new socket connection so we can send updates to it as they come up
        self.websockets.append(ws)

        # Read inbound messages from websocket
        async for msg in ws:
            # We don't actually care about inbound messages, so we drop them on the floor unless they're errors
            if msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
        print('websocket connection closed')

        # Once the "async for" loop is done, we know the WebSocket is closed

        # Filter out the newly-closed socket from the server's list of sockets
        self.websockets = [socket for socket in self.websockets if socket != ws]
        return ws

    async def _handle_new_data(self, new_data):
        # Iterate over the conencted websockets
        for ws in self.websockets:
            # Send the new data to each websocket as a string
            await ws.send_str(str(new_data))

    async def _start_background_tasks(self, app):
        # Create the background job
        some_background_job = SomeBackgroundJob(self._handle_new_data)
        # Create a "Task" to run in the background that runs the connector
        app['connector_task'] = asyncio.create_task(some_background_job.run())

    async def _cleanup_background_tasks(self, app):
        # We are shutting down the app, so we should cancel the task
        app['connector_task'].cancel()
        await app['connector_task']
