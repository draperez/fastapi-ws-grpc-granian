import json
from fastapi import WebSocket

class WSConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, connection: WebSocket):
        await connection.accept()
        self.active_connections.append(connection)

    def disconnect(self, connection: WebSocket):
        self.active_connections.remove(connection)

    async def clear_all_connections(self):
        for connection in self.active_connections:
            try:
                await self.send_message_to_client(connection, {"message": "Server is shutting down, closing connection."})
                await connection.close()
            except Exception as e:
                # Connection might already be closed
                pass
        self.active_connections.clear()

    async def send_message_to_client(self, connection: WebSocket, message: dict):
        await connection.send_text(json.dumps(message))

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await self.send_message_to_client(connection, message)