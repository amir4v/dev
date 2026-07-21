#!/bin/bash
set -e

# 1. Install Xray-core (Idempotent)
if ! command -v xray &> /dev/null; then
    echo "Installing Xray-core..."
    apt install -y curl unzip openssl
    curl -L https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip -o xray.zip
    unzip -o xray.zip -d /usr/local/bin/
    rm -f xray.zip geoip.dat geosite.dat
else
    echo "Xray-core already installed."
fi

# 2. Generate Random Parameters
PORT=$(shuf -i 10000-65000 -n 1)
UUID=$(cat /proc/sys/kernel/random/uuid)
ALTER_ID=0

# 3. Generate Self-Signed Certificate
CERT_DIR="/etc/xray/certs"
mkdir -p $CERT_DIR
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout $CERT_DIR/key.pem \
    -out $CERT_DIR/cert.pem \
    -subj "/CN=xray.local" 2>/dev/null

# 4. Create Xray Configuration
mkdir -p /usr/local/etc/xray
tee /usr/local/etc/xray/config.json > /dev/null <<EOF
{
  "inbounds": [{
    "port": ${PORT},
    "protocol": "vmess",
    "settings": {
      "clients": [{
        "id": "${UUID}",
        "alterId": ${ALTER_ID}
      }]
    },
    "streamSettings": {
      "network": "tcp",
      "security": "tls",
      "tlsSettings": {
        "certificates": [{
          "certificateFile": "${CERT_DIR}/cert.pem",
          "keyFile": "${CERT_DIR}/key.pem"
        }]
      }
    }
  }],
  "outbounds": [{
    "protocol": "freedom"
  }]
}
EOF

# 5. Create Systemd Service (Idempotent)
if [ ! -f /etc/systemd/system/xray.service ]; then
    tee /etc/systemd/system/xray.service > /dev/null <<EOF
[Unit]
Description=Xray Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/xray run -config /usr/local/etc/xray/config.json
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
    systemctl daemon-reload
fi

# 6. Enable and Start
systemctl enable xray
systemctl restart xray

# 7. Open Firewall
# ufw allow ${PORT}/tcp

# 8. Generate and Output Base64 VMess Link
SERVER_IP=$(curl -s ifconfig.me)
VMESS_JSON="{\"v\":\"2\",\"ps\":\"VMess\",\"add\":\"${SERVER_IP}\",\"port\":\"${PORT}\",\"id\":\"${UUID}\",\"aid\":\"${ALTER_ID}\",\"net\":\"tcp\",\"type\":\"none\",\"host\":\"\",\"path\":\"\",\"tls\":\"tls\"}"
VMESS_LINK="vmess://$(echo -n $VMESS_JSON | base64 -w 0)"

echo ""
echo "=== VMess Connection Ready ==="
echo "$VMESS_LINK"
echo "=============================="
echo "Note: Clients must disable 'Verify Certificate' for self-signed certs."