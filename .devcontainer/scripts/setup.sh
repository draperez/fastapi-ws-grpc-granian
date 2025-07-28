#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
else
    echo "Virtual environment already exists."
fi

echo "Installing Python packages"
if [ -f pyproject.toml ]; then 
    uv sync --extra dev;
elif [ -f requirements.txt ]; then 
    uv pip install -r requirements.txt; 
fi

# Create the dev-certs with proper SANs
mkdir -p ~/dev-certs

# Create a config file for the certificate with SANs
cat > ~/dev-certs/cert.conf << EOF
[req]
default_bits = 2048
prompt = no
default_md = sha256
distinguished_name = dn
req_extensions = v3_req

[dn]
CN=localhost

[v3_req]
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = *.localhost
IP.1 = 127.0.0.1
IP.2 = ::1
EOF

# Generate certificate with SANs
openssl req -x509 -newkey rsa:2048 -keyout ~/dev-certs/key.pem -out ~/dev-certs/cert.pem -days 365 -nodes -config ~/dev-certs/cert.conf -extensions v3_req

# Clean up the config file
rm ~/dev-certs/cert.conf

# Install grpcurl
echo "Installing grpcurl..."
mkdir -p ~/bin
curl -L https://github.com/fullstorydev/grpcurl/releases/download/v1.8.9/grpcurl_1.8.9_linux_x86_64.tar.gz -o ~/bin/grpcurl.tar.gz
tar -xz -C ~/bin -f ~/bin/grpcurl.tar.gz
rm ~/bin/grpcurl.tar.gz
echo "grpcurl installed to ~/bin/grpcurl"

# Add ~/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
    echo "Added ~/bin to PATH in ~/.bashrc"
fi