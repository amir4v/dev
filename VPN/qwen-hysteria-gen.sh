#!/bin/bash
set -e

# --- Configuration ---
DOMAIN="amir4v.ir" # <--- CHANGE THIS
EMAIL="amir4vx@gmail.com" # <--- CHANGE THIS

# 1. Install Dependencies & Hysteria2 Server
echo "Installing dependencies..."
apt install -y curl certbot python3-certbot-nginx

# Download latest Hysteria2 server
HY_VERSION="2.4.2"
curl -L https://github.com/apernet/hysteria/releases/download/app/v${HY_VERSION}/hysteria-linux-amd64 -o /usr/local/bin/hysteria
chmod +x /usr/local/bin/hysteria

# 2. Generate Random Parameters
PORT=$(shuf -i 10000-65000 -n 1)
PASSWORD=$(openssl rand -base64 32)

# 3. Obtain Real TLS Certificate
echo "Obtaining TLS certificate for ${DOMAIN}..."
certbot certonly --standalone --non-interactive --agree-tos --email ${EMAIL} -d ${DOMAIN}

CERT_PATH="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/${DOMAIN}/privkey.pem"

# 4. Create Hysteria2 Configuration
mkdir -p /etc/hysteria
tee /etc/hysteria/config.yaml > /dev/null <<EOF
listen: :${PORT}

tls:
  cert: ${CERT_PATH}
  key: ${KEY_PATH}

auth:
  type: password
  password: ${PASSWORD}

bandwidth:
  up: 100 mbps
  down: 100 mbps

ignoreClientBandwidth: false

masquerade:
  type: proxy
  proxy:
    url: https://www.bing.com
    rewriteHost: true
EOF

# 5. Create Systemd Service
tee /etc/systemd/system/hysteria.service > /dev/null <<EOF
[Unit]
Description=Hysteria2 Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/hysteria server -c /etc/hysteria/config.yaml
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable and Start
systemctl daemon-reload
systemctl enable hysteria
systemctl restart hysteria

# 7. Open Firewall (UDP)
ufw allow ${PORT}/udp

# 8. Output Connection String
echo ""
echo "=== Hysteria2 Connection Ready ==="
echo "hysteria2://${PASSWORD}@${DOMAIN}:${PORT}?insecure=0&sni=${DOMAIN}&mport=${PORT}#Hysteria2"
echo "=================================="
echo "Note: Use a Hysteria2 compatible client (e.g., NekoBox, FlClash, Clash Verge)."