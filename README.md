# Granian with FastAPI

Testing Granian Rust server for Python with FastAPI.

Debugging works using `debugpy` and `granian` (see `.vscode/launch.json`).

Another way to run the server:

```bash
uv run granian --interface asgi --ssl-certificate ~/dev-certs/cert.pem --ssl-keyfile ~/dev-certs/key.pem main:app
```

Devcontainer has created a self signed certificate for HTTPS at `~/dev-certs/cert.pem` and `~/dev-certs/cert.key`.

> [WARNING] Certificates are mandatory if we want to use HTTP/2, otherwise HTTP/1.1 will be used.

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

```bash
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. --proto_path=./proto myservice.proto
```

After that `myservice_pb2.py` and `myservice_pb2_grpc.py` files will be created in the current directory.