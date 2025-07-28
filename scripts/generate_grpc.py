#!/usr/bin/env python3
"""
Script to generate gRPC protobuf files from .proto definitions.
"""

import subprocess
import sys
from pathlib import Path

def generate_grpc_files():
    """Generate gRPC protobuf files."""
    project_root = Path(__file__).parent.parent
    proto_dir = project_root / "proto"
    output_dir = project_root / "src" / "grpc" / "generated"
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Find all .proto files
    proto_files = list(proto_dir.glob("*.proto"))
    
    if not proto_files:
        print("No .proto files found in proto/ directory")
        return False
    
    for proto_file in proto_files:
        print(f"Generating protobuf files for {proto_file.name}...")
        
        cmd = [
            sys.executable, "-m", "grpc_tools.protoc",
            f"--python_out={output_dir}",
            f"--grpc_python_out={output_dir}",
            f"--proto_path={proto_dir}",
            str(proto_file)
        ]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print(f"✓ Successfully generated files for {proto_file.name}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error generating files for {proto_file.name}:")
            print(f"  {e.stderr}")
            return False
    
    print(f"\nGenerated files in: {output_dir}")
    return True

if __name__ == "__main__":
    if generate_grpc_files():
        print("All protobuf files generated successfully!")
    else:
        print("Failed to generate some protobuf files.")
        sys.exit(1)
