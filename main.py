
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from ws_connection_manager import WSConnectionManager
from grpc_service import serve_grpc

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

ws_manager = WSConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting gRPC server...")
    grpc_task = asyncio.create_task(serve_grpc())
    yield
    logger.info("Shutting down gRPC server...")
    grpc_task.cancel()
    await ws_manager.clear_all_connections()

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root_ep():
    return FileResponse("static/index.html")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
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

