import asyncio
from websockets import serve


class WebSocketServer:
    connection = None

    def __init__(self):
        pass

    def start(self):
        asyncio.run(self._start())

    async def _start(self):
        port = 8765
        async with serve(self.onMessage, "0.0.0.0", port):
            print("Listening to ws://0.0.0.0:%d" % 8765)
            await asyncio.Future()  # run forever

    async def onMessage(self, websocket):
        self.connection = websocket  # Store the connection to whichever client messaged last
        async for message in websocket:
            print("Received message: %s" % message)
            await websocket.send(message)

    async def send(self, message):
        if self.connection:
            try:
                # print("Sending '%s'" % message)
                await self.connection.send(message)
            except Exception as e:
                print("WS send() Exception: " + str(e))
                self.connection = None


# async def wsmain():
#     async with serve(self.onMessage, "0.0.0.0", 8765):
#         print("Listening to ws://0.0.0.0:8765")
#         await asyncio.Future()  # run forever
