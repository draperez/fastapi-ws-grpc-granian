# Granian with FastAPI

FastAPI application with WS and gRPC using Granian Rust server for Python.

## Project Structure

```
├── src/
│   ├── api/               # FastAPI routes and endpoints
│   ├── grpc/              # gRPC service implementation
│   │   ├── generated/     # Auto-generated protobuf files
│   │   └── service.py     # gRPC service logic
│   ├── websocket/         # WebSocket connection management
│   ├── app.py             # Main FastAPI application
│   └── config.py          # Application configuration
├── proto/                 # Protocol buffer definitions
├── static/                # Static web assets
├── scripts/               # Utility scripts
├── tests/                 # Test suite
└── main_new.py           # Application entry point
```

## Running the Server

> [WARNING] Certificates are mandatory if we want to use HTTP/2, otherwise HTTP/1.1 will be used.

### For development and debugging

Just press `F5` in VSCode to start the server with debugging enabled (see `.vscode/launch.json`).

### Using Granian directly

```bash
uv run granian --interface asgi --ssl-certificate ~/dev-certs/cert.pem --ssl-keyfile ~/dev-certs/key.pem src.app:app
```

### Running main.py

```bash
uv run python main.py
```


## Calling gRPC service

During devcontainer setup, a gRPC client has been installed (`grpcurl`). You can use it to test the gRPC service.

### With SSL (Recommended - matches server configuration):

```bash
# List all services
grpcurl -insecure localhost:8001 list

# List methods of a service
grpcurl -insecure localhost:8001 list myservice.MyService

# Call method without data
grpcurl -insecure localhost:8001 myservice.MyService.MyMethod

# Call method with data
grpcurl -d '{"name": "Mundua"}' -insecure localhost:8001 myservice.MyService.MyMethod
```

### Without SSL (if server falls back to insecure mode):

```bash
# List all services
grpcurl -plaintext localhost:8001 list

# List methods of a service
grpcurl -plaintext localhost:8001 list myservice.MyService

# Call method without data
grpcurl -plaintext localhost:8001 myservice.MyService.MyMethod

# Call method with data
grpcurl -d '{"name": "Mundua"}' -plaintext localhost:8001 myservice.MyService.MyMethod
```

## Create gRPC PB2 files

Use the provided script to generate protobuf files:

```bash
uv run python scripts/generate_grpc.py
```

Or manually:

```bash
python -m grpc_tools.protoc --python_out=src/grpc/generated --grpc_python_out=src/grpc/generated --proto_path=./proto myservice.proto
```

After that `myservice_pb2.py` and `myservice_pb2_grpc.py` files will be created in `src/grpc/generated/`.

## Development

### Installing dependencies

```bash
# Install main dependencies
uv sync

# Install development dependencies
uv sync --extra dev
```

### Running tests

```bash
uv run pytest
```
