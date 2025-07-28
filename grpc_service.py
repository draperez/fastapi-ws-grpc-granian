import os
import grpc
import logging
from concurrent import futures
from grpc_reflection.v1alpha import reflection
import myservice_pb2_grpc
import myservice_pb2

logger = logging.getLogger(__name__)

async def serve_grpc():
    logger.info("Starting gRPC server...")
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    myservice_pb2_grpc.add_MyServiceServicer_to_server(MyGrpcService(), server)

    SERVICE_NAMES = (
        myservice_pb2.DESCRIPTOR.services_by_name['MyService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    cert_path = os.getenv('GRPC_CERT_PATH', '~/dev-certs/cert.pem')
    key_path = os.getenv('GRPC_KEY_PATH', '~/dev-certs/key.pem')
    
    try:
        # Expand user paths and check if files exist
        cert_path_expanded = os.path.expanduser(cert_path)
        key_path_expanded = os.path.expanduser(key_path)
        
        if not os.path.exists(cert_path_expanded):
            raise FileNotFoundError(f"Certificate file not found: {cert_path_expanded}")
        if not os.path.exists(key_path_expanded):
            raise FileNotFoundError(f"Private key file not found: {key_path_expanded}")
        
        with open(cert_path_expanded, 'rb') as f:
            certificate_chain = f.read()
        with open(key_path_expanded, 'rb') as f:
            private_key = f.read()
        
        # Validate certificate format
        if not certificate_chain.startswith(b'-----BEGIN CERTIFICATE-----'):
            raise ValueError("Invalid certificate format - must be PEM encoded")
        if not private_key.startswith(b'-----BEGIN PRIVATE KEY-----'):
            raise ValueError("Invalid private key format - must be PEM encoded")
        
        # Create SSL server credentials
        server_credentials = grpc.ssl_server_credentials(
            private_key_certificate_chain_pairs=[(private_key, certificate_chain)],
            root_certificates=None,  # No client certificate verification
            require_client_auth=False
        )
        server.add_secure_port('[::]:8001', server_credentials)
        logger.info("gRPC server started with SSL on port 8001")
        logger.info("Use 'grpcurl -insecure localhost:8001 list' to test with SSL")
    except Exception as e:
        logger.error("Failed to start gRPC server with SSL: %s", e)
        logger.info("Starting gRPC server without SSL on port 8001")
        logger.info("Use 'grpcurl -plaintext localhost:8001 list' to test without SSL")
        server.add_insecure_port('[::]:8001')

    await server.start()
    logger.info("gRPC server started on port 8001")
    await server.wait_for_termination()

class MyGrpcService(myservice_pb2_grpc.MyServiceServicer):
    async def MyMethod(self, request, context):
        logger.debug("Received request: %s", request)
        # Implement your gRPC method logic here
        name = request.name if request.name else "World"
        response = myservice_pb2.MyResponse()
        response.message = f"Kaixo {name}!"
        return response

