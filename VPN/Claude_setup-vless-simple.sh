#!/usr/bin/env bash
set -e

# Install Nginx
apt install -y nginx
systemctl stop nginx
# Install Xray core (if not already via 3X-UI)
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
# Install Certbot
apt install -y certbot

# ==== EDIT THESE ====
DOMAIN="yek.yourdomain.com"
WS_PATH="/lives"
EXT_PORT="443"
XRAY_PORT="10000"
CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
KEY_PATH="/etc/letsencrypt/live/$DOMAIN/privkey.pem"
CLIENT_NAME="MyServer"
# =====================

UUID=$(cat /proc/sys/kernel/random/uuid)

cat > /usr/local/etc/xray/config.json <<EOF
{
  "inbounds": [{
    "listen": "127.0.0.1",
    "port": $XRAY_PORT,
    "protocol": "vless",
    "settings": { "clients": [{ "id": "$UUID", "level": 0 }], "decryption": "none" },
    "streamSettings": { "network": "ws", "wsSettings": { "path": "$WS_PATH" } }
  }],
  "outbounds": [{ "protocol": "freedom" }]
}
EOF

cat > /etc/nginx/sites-available/vless <<EOF
server {
    listen $EXT_PORT ssl;
    server_name $DOMAIN;
    ssl_certificate $CERT_PATH;
    ssl_certificate_key $KEY_PATH;

    location $WS_PATH {
        proxy_pass http://127.0.0.1:$XRAY_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }
}
EOF

ln -sf /etc/nginx/sites-available/vless /etc/nginx/sites-enabled/vless
nginx -t
systemctl enable --now xray
systemctl restart xray
systemctl restart nginx

echo "# How to undo: #"
echo " systemctl stop xray nginx "
echo " rm -f /etc/nginx/sites-enabled/vless /etc/nginx/sites-available/vless "
echo " rm -f /usr/local/etc/xray/config.json "
echo " systemctl start nginx "
echo "."

echo "vless://$UUID@$DOMAIN:$EXT_PORT?encryption=none&security=tls&sni=$DOMAIN&fp=chrome&type=ws&host=$DOMAIN&path=$(python3 -c "import urllib.parse,sys;print(urllib.parse.quote(sys.argv[1]))" "$WS_PATH")#$CLIENT_NAME"
