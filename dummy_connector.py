import asyncio
from datetime import datetime


class Connector:
    def __init__(self, handle_new_data):
        self.handle_new_data = handle_new_data

    async def start_exchanges(self):
        while True:
            await asyncio.sleep(1),
            await self.handle_new_data(datetime.now())
