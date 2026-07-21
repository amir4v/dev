#!/bin/bash
set -e

# 1. Install WireGuard (Idempotent)
if ! command -v wg &> /dev/null; then
    echo "Installing WireGuard..."
    apt install -y wireguard qrencode
else
    echo "WireGuard already installed."
fi

# 2. Generate Server Keys
SERVER_PRIVATE_KEY=$(wg genkey)
SERVER_PUBLIC_KEY=$(echo $SERVER_PRIVATE_KEY | wg pubkey)

# 3. Generate Client Keys
CLIENT_PRIVATE_KEY=$(wg genkey)
CLIENT_PUBLIC_KEY=$(echo $CLIENT_PRIVATE_KEY | wg pubkey)

# 4. Network Configuration
PORT=$(shuf -i 10000-65000 -n 1)
SERVER_IP="10.0.0.1"
CLIENT_IP="10.0.0.2"
SUBNET="24"

# 5. Create Server Configuration
tee /etc/wireguard/wg0.conf > /dev/null <<EOF
[Interface]
PrivateKey = ${SERVER_PRIVATE_KEY}
Address = ${SERVER_IP}/${SUBNET}
ListenPort = ${PORT}

[Peer]
PublicKey = ${CLIENT_PUBLIC_KEY}
AllowedIPs = ${CLIENT_IP}/32
EOF

# 6. Set Permissions and Start
chmod 600 /etc/wireguard/wg0.conf
systemctl enable wg-quick@wg0
systemctl restart wg-quick@wg0

# 7. Open Firewall
# ufw allow ${PORT}/udp

# 8. Generate Client Configuration
SERVER_IP_PUBLIC=$(curl -s ifconfig.me)
CLIENT_CONF="[Interface]
PrivateKey = ${CLIENT_PRIVATE_KEY}
Address = ${CLIENT_IP}/${SUBNET}
DNS = 1.1.1.1

[Peer]
PublicKey = ${SERVER_PUBLIC_KEY}
Endpoint = ${SERVER_IP_PUBLIC}:${PORT}
AllowedIPs = 0.0.0.0/0"

# 9. Output Results
echo ""
echo "=== WireGuard Connection Ready ==="
echo "Server Port: ${PORT}"
echo ""
echo "--- Client Config (Save as wg0.conf) ---"
echo "$CLIENT_CONF"
echo "----------------------------------------"
echo ""
echo "--- QR Code for Mobile Clients ---"
echo "$CLIENT_CONF" | qrencode -t ANSIUTF8
echo "=================================="