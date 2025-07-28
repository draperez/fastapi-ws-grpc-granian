import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routes import router
from src.grpc.service import serve_grpc
from src.websocket.connection_manager import WSConnectionManager

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

ws_manager = WSConnectionManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting gRPC server...")
    grpc_task = asyncio.create_task(serve_grpc())
    
    try:
        yield
    finally:
        logger.info("Shutting down gRPC server...")
        grpc_task.cancel()
        
        try:
            await grpc_task
        except asyncio.CancelledError:
            logger.info("gRPC server task cancelled successfully")
        
        await ws_manager.clear_all_connections()
        logger.info("All connections cleared")

def create_app() -> FastAPI:
    app = FastAPI(
        title="Granian FastAPI Server",
        description="FastAPI application with gRPC and WebSocket support",
        version="0.1.0",
        lifespan=lifespan
    )

    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Include API routes
    app.include_router(router)
    
    return app

app = create_app()
