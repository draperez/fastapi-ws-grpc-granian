from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

from ..websocket.connection_manager import WSConnectionManager

router = APIRouter()
ws_manager = WSConnectionManager()

@router.get("/")
async def root_endpoint():
    """Serve the main HTML page."""
    return FileResponse("static/index.html")

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handle WebSocket connections."""
    message = {
        "client": websocket.client.port,
        "data": "Connected"
    }
    await ws_manager.broadcast(message)

    await ws_manager.connect(websocket)
    await ws_manager.send_message_to_client(websocket, {
        "your_client": websocket.client.port,
        "data": "Welcome to the WebSocket server!",
        "client": "server"
    })

    try:
        data = ""
        while data != "exit":
            data = await websocket.receive_text()
            if data == "exit":
                message["data"] = "Bye!"
                await ws_manager.send_message_to_client(websocket, message)
            else:
                message["data"] = data
                await ws_manager.broadcast(message)
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
        message["data"] = "Disconnected"
        await ws_manager.broadcast(message)
