#!/bin/bash
set -e

# 1. Install Xray-core (Idempotent)
if ! command -v xray &> /dev/null; then
    echo "Installing Xray-core..."
    apt install -y curl unzip
    curl -L https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip -o xray.zip
    unzip -o xray.zip -d /usr/local/bin/
    rm -f xray.zip geoip.dat geosite.dat
else
    echo "Xray-core already installed."
fi

# 2. Generate Random Parameters
PORT=$(shuf -i 10000-65000 -n 1)
UUID=$(cat /proc/sys/kernel/random/uuid)

# 3. Create Xray Configuration (No TLS)
mkdir -p /usr/local/etc/xray
tee /usr/local/etc/xray/config.json > /dev/null <<EOF
{
  "inbounds": [{
    "port": ${PORT},
    "protocol": "vless",
    "settings": {
      "clients": [{
        "id": "${UUID}",
        "level": 0,
        "encryption": "none"
      }],
      "decryption": "none"
    },
    "streamSettings": {
      "network": "tcp",
      "security": "none"
    }
  }],
  "outbounds": [{
    "protocol": "freedom"
  }]
}
EOF

# 4. Create Systemd Service (Idempotent)
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

# 5. Enable and Start
systemctl enable xray
systemctl restart xray

# 6. Open Firewall
# ufw allow ${PORT}/tcp

# 7. Output Connection String
SERVER_IP=$(curl -s ifconfig.me)
echo ""
echo "=== VLESS Connection Ready (No TLS) ==="
echo "vless://${UUID}@${SERVER_IP}:${PORT}?encryption=none&security=none&type=tcp#VLESS"
echo "======================================="