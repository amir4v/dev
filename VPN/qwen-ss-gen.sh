# 1. Install Shadowsocks-libev
apt install -y shadowsocks-libev

# 2. Generate random strong parameters
PORT=$(shuf -i 10000-65000 -n 1)
PASSWORD=$(openssl rand -base64 32)
METHODS=("aes-256-gcm" "chacha20-ietf-poly1305")
METHOD=${METHODS[$RANDOM % ${#METHODS[@]}]}

# 3. Create configuration file
tee /etc/shadowsocks-libev/config.json > /dev/null <<EOF
{
    "server":"0.0.0.0",
    "server_port":${PORT},
    "password":"${PASSWORD}",
    "timeout":300,
    "method":"${METHOD}"
}
EOF

# 4. Enable and start service
systemctl enable shadowsocks-libev
systemctl restart shadowsocks-libev

# 5. Get server IP
SERVER_IP=$(curl -s ifconfig.me)

# 6. Output ready-to-use connection string
echo "ss://${METHOD}:${PASSWORD}@${SERVER_IP}:${PORT}"