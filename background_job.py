import asyncio
from datetime import datetime


class SomeBackgroundJob:
    def __init__(self, update_handler):
        self.update_handler = update_handler

    async def run(self):
        while True:
            await asyncio.sleep(1),
            await self.update_handler(datetime.now())
