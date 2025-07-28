"""
Application configuration settings.
"""

import os
from pathlib import Path

# Server configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
GRPC_PORT = int(os.getenv("GRPC_PORT", "8001"))

# SSL configuration
CERT_DIR = Path.home() / "dev-certs"
SSL_CERT_PATH = CERT_DIR / "cert.pem"
SSL_KEY_PATH = CERT_DIR / "key.pem"

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Static files
STATIC_DIR = "static"
