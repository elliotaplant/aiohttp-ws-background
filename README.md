# aiohttp Background Job With WebSocket Updates Demo
This repo is an example of how to to
- Start an http server with [aiohttp](https://docs.aiohttp.org/en/stable/)
- Create a route on that server to [serve WebSockets](https://docs.aiohttp.org/en/stable/web_quickstart.html#websockets)
- Start a [background job](https://docs.aiohttp.org/en/stable/web_advanced.html#background-tasks) with that server
- Send updates from the background job to all open WebSocket connections
- Receive and parse those updates in JavaScript
- Update the HTML of a page with JavaScript based on received updates
