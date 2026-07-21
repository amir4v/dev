#!/bin/bash
set -e

# --- Configuration ---
DOMAIN="amir4v.ir" # <--- CHANGE THIS
EMAIL="amir4vx@gmail.com" # <--- CHANGE THIS

# 1. Install Dependencies & Tuic Server
echo "Installing dependencies..."
apt install -y curl certbot python3-certbot-nginx

# Download latest Tuic server (Check GitHub for latest version if this fails)
TUIC_VERSION="1.0.0" 
curl -L https://github.com/EAimTY/tuic/releases/download/${TUIC_VERSION}/tuic-server-${TUIC_VERSION}-x86_64-unknown-linux-gnu -o /usr/local/bin/tuic-server
chmod +x /usr/local/bin/tuic-server

# 2. Generate Random Parameters
PORT=$(shuf -i 10000-65000 -n 1)
UUID=$(cat /proc/sys/kernel/random/uuid)
PASSWORD=$(openssl rand -base64 16)

# 3. Obtain Real TLS Certificate
echo "Obtaining TLS certificate for ${DOMAIN}..."
certbot certonly --standalone --non-interactive --agree-tos --email ${EMAIL} -d ${DOMAIN}

CERT_PATH="/etc/letsencrypt/live/${DOMAIN}/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/${DOMAIN}/privkey.pem"

# 4. Create Tuic Configuration
mkdir -p /etc/tuic
tee /etc/tuic/config.json > /dev/null <<EOF
{
    "server": "[::]:${PORT}",
    "users": {
        "${UUID}": "${PASSWORD}"
    },
    "certificate": "${CERT_PATH}",
    "private_key": "${KEY_PATH}",
    "congestion_control": "bbr",
    "alpn": ["h3", "spdy/3.1"],
    "zero_rtt_handshake": false,
    "heartbeat": "3s",
    "timeout": "8s",
    "max_idle_time": "10s",
    "auth_timeout": "3s",
    "task_negotiation_timeout": "3s",
    "max_udp_relay_packet_size": 1500
}
EOF

# 5. Create Systemd Service
tee /etc/systemd/system/tuic.service > /dev/null <<EOF
[Unit]
Description=Tuic Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/tuic-server -c /etc/tuic/config.json
Restart=on-failure
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
EOF

# 6. Enable and Start
systemctl daemon-reload
systemctl enable tuic
systemctl restart tuic

# 7. Open Firewall (UDP)
# ufw allow ${PORT}/udp

# 8. Output Connection Details
SERVER_IP=$(curl -s ifconfig.me)
echo ""
echo "=== Tuic Connection Ready ==="
echo "Server: ${DOMAIN}"
echo "Port: ${PORT}"
echo "UUID: ${UUID}"
echo "Password: ${PASSWORD}"
echo "Congestion: bbr"
echo "ALPN: h3"
echo "============================="
echo "Note: Use a Tuic v5 compatible client (e.g., NekoBox, FlClash)."