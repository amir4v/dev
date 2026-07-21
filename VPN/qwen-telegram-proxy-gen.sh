#!/bin/bash
set -e

# 1. Install MTProto Proxy (Docker method for reliability)
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable --now docker
fi

# 2. Generate Random Parameters
PORT=$(shuf -i 10000-65000 -n 1)
SECRET=$(openssl rand -hex 16)
TAG="amir_proxy"

# 3. Run MTProto Proxy Container
echo "Starting MTProto Proxy..."
docker run -d \
    --name mtproto-proxy \
    --restart always \
    -p ${PORT}:${PORT} \
    -e SECRET=${SECRET} \
    -e TAG=${TAG} \
    telegrammessenger/proxy:latest

# 4. Get Server IP
SERVER_IP=$(curl -s ifconfig.me)

# 5. Output Connection String
# Format: tg://proxy?server=IP&port=PORT&secret=SECRET
echo ""
echo "=== Telegram Proxy Ready ==="
echo "tg://proxy?server=${SERVER_IP}&port=${PORT}&secret=${SECRET}"
echo "============================"
echo "Click the link above on a device with Telegram installed to connect."