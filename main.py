"""
Main entry point for the Granian FastAPI application.
"""

import signal
import sys
from src.app import app
from src.config import HOST, PORT, SSL_CERT_PATH, SSL_KEY_PATH


def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    print(f"\nReceived signal {signum}. Shutting down gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    import granian
    from granian.constants import Interfaces
    
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check if SSL certificates exist
    if SSL_CERT_PATH.exists() and SSL_KEY_PATH.exists():
        print(f"Starting Granian server with SSL on {HOST}:{PORT}")
        print(f"Using certificates: {SSL_CERT_PATH} and {SSL_KEY_PATH}")
        
        granian.Granian(
            "src.app:app",
            address=HOST,
            port=PORT,
            interface=Interfaces.ASGI,
            ssl_cert=SSL_CERT_PATH,
            ssl_key=SSL_KEY_PATH,
        ).serve()
    else:
        print(f"Starting Granian server without SSL on {HOST}:{PORT}")
        print("Warning: SSL certificates not found, running in insecure mode")
        
        granian.Granian(
            "src.app:app",
            address=HOST,
            port=PORT,
            interface=Interfaces.ASGI,
        ).serve()
