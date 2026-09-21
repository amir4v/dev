#!/bin/bash
set -e

PORT=8443
PASS=$(openssl rand -base64 18)
METHOD=chacha20-ietf-poly1305

apt-get update -qq
apt-get install -yqq shadowsocks-libev curl

cat >/etc/shadowsocks-libev/config.json <<EOF
{
  "server": "0.0.0.0",
  "server_port": $PORT,
  "password": "$PASS",
  "method": "$METHOD",
  "mode": "tcp_and_udp"
}
EOF

ufw allow $PORT >/dev/null 2>&1 || true
systemctl enable --now shadowsocks-libev
systemctl restart shadowsocks-libev

USERINFO=$(printf '%s:%s' "$METHOD" "$PASS" | base64 -w0 | tr '+/' '-_' | tr -d =)
echo "ss://$USERINFO@$(curl -s4 ifconfig.me):$PORT#ss"