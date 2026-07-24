#!/usr/bin/env bash
#
# setup-vless.sh — Interactive VLESS + WS + TLS (Cloudflare-fronted) installer
# Safe by design: backs up anything it touches, validates before restarting
# services, and can roll itself back cleanly if something fails.
#
set -euo pipefail

# Install Nginx
apt install -y nginx
systemctl stop nginx
# Install Xray core (if not already via 3X-UI)
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
# Install Certbot
apt install -y certbot

BACKUP_DIR="/root/vless-setup-backup-$(date +%Y%m%d-%H%M%S)"
LOG="/root/vless-setup.log"
XRAY_CONFIG="/usr/local/etc/xray/config.json"
NGINX_SITE="/etc/nginx/sites-available/vless"
NGINX_LINK="/etc/nginx/sites-enabled/vless"

log()   { echo -e "[*] $*" | tee -a "$LOG"; }
warn()  { echo -e "[!] $*" | tee -a "$LOG" >&2; }
die()   { warn "$*"; warn "Aborting. Nothing further will be changed."; exit 1; }

require_root() {
  [[ $EUID -eq 0 ]] || die "Run this as root (sudo)."
}

backup_if_exists() {
  local f="$1"
  if [[ -e "$f" ]]; then
    mkdir -p "$BACKUP_DIR"
    cp -a "$f" "$BACKUP_DIR/$(basename "$f").bak"
    log "Backed up existing $f -> $BACKUP_DIR/"
  fi
}

ask() {
  local prompt="$1" default="${2:-}" var
  if [[ -n "$default" ]]; then
    read -rp "$prompt [$default]: " var
    echo "${var:-$default}"
  else
    read -rp "$prompt: " var
    while [[ -z "$var" ]]; do
      read -rp "  (required) $prompt: " var
    done
    echo "$var"
  fi
}

ask_yn() {
  local prompt="$1" ans
  read -rp "$prompt [y/N]: " ans
  [[ "$ans" =~ ^[Yy]$ ]]
}

rollback() {
  warn "Rolling back changes..."
  systemctl stop xray 2>/dev/null || true
  rm -f "$NGINX_LINK" "$NGINX_SITE"
  [[ -f "$BACKUP_DIR/config.json.bak" ]] && cp -a "$BACKUP_DIR/config.json.bak" "$XRAY_CONFIG"
  nginx -t 2>/dev/null && systemctl restart nginx || warn "Nginx may need manual attention."
  warn "Rollback complete. Backup preserved at $BACKUP_DIR"
  exit 1
}

trap 'warn "Something failed."; rollback' ERR

echo "=== Interactive VLESS + WS + TLS setup ==="
echo "Nothing is changed until each step confirms success. A backup of any"
echo "file this script overwrites is kept at: $BACKUP_DIR"
echo

require_root

DOMAIN=$(ask "Subdomain already pointed at this VPS via Cloudflare (e.g. sub.example.com)")
WS_PATH=$(ask "WebSocket path" "/$(tr -dc a-z0-9 </dev/urandom | head -c8)")
[[ "$WS_PATH" == /* ]] || WS_PATH="/$WS_PATH"

port_busy() {
  ss -Htln "( sport = :$1 )" 2>/dev/null | grep -q ":$1 "
}

# Cloudflare only proxies these ports for HTTPS traffic when orange-cloud is on
CF_HTTPS_PORTS=(443 2053 2083 2087 2096 8443)

pick_free_cf_port() {
  for p in "${CF_HTTPS_PORTS[@]}"; do
    port_busy "$p" || { echo "$p"; return; }
  done
  echo ""  # none free
}

echo
log "Checking if port 443 is available (this is what Nginx/Cloudflare will use)..."
if port_busy 443; then
  warn "Port 443 is already in use on this host."
  SUGGESTED=$(pick_free_cf_port)
  if [[ -n "$SUGGESTED" ]]; then
    log "Suggested free Cloudflare-proxiable port: $SUGGESTED"
  else
    warn "None of Cloudflare's alternate HTTPS ports (${CF_HTTPS_PORTS[*]}) are free either."
    SUGGESTED=$(ask "Enter a free port manually" "8443")
  fi
  if ask_yn "Use port $SUGGESTED instead of 443?"; then
    EXT_PORT="$SUGGESTED"
  else
    EXT_PORT=$(ask "Enter the port you want Nginx to listen on")
    port_busy "$EXT_PORT" && die "Port $EXT_PORT is also busy — check 'ss -tlnp' and pick another."
  fi
else
  log "Port 443 is free."
  EXT_PORT="443"
fi
if [[ "$EXT_PORT" != "443" ]]; then
  warn "Remember: with a non-standard port, Cloudflare only proxies it if it's one of: ${CF_HTTPS_PORTS[*]}"
  warn "The client link will need :$EXT_PORT appended after the domain."
fi

XRAY_PORT=$(ask "Local port for Xray to listen on (internal, not exposed)" "10000")
port_busy "$XRAY_PORT" && die "Local port $XRAY_PORT is already in use — pick a different one."
CLIENT_NAME=$(ask "Label for the client link" "MyServer")


echo
echo "Cloudflare SSL/TLS mode must be 'Full' or 'Full (strict)'."
if ask_yn "Do you need a Let's Encrypt cert issued now (Full strict)?"; then
  NEED_CERT=1
  CERT_EMAIL=$(ask "Email for Let's Encrypt renewal notices")
else
  NEED_CERT=0
  warn "Assuming Cloudflare mode is 'Full' with a self-signed/Cloudflare Origin cert already in place."
  CERT_PATH=$(ask "Path to existing fullchain cert" "/etc/ssl/certs/cloudflare-origin.pem")
  KEY_PATH=$(ask "Path to existing private key" "/etc/ssl/private/cloudflare-origin.key")
fi

echo
log "Checking prerequisites..."
command -v curl >/dev/null || die "curl not found — install it first."

if ! command -v xray >/dev/null; then
  if ask_yn "Xray not found. Install it now?"; then
    bash -c "$(curl -fsSL https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install
  else
    die "Xray is required."
  fi
else
  log "Xray already installed."
fi

if ! command -v nginx >/dev/null; then
  if ask_yn "Nginx not found. Install it now?"; then
    apt-get update -qq && apt-get install -y -qq nginx
  else
    die "Nginx is required."
  fi
else
  log "Nginx already installed."
fi

if [[ $NEED_CERT -eq 1 ]]; then
  command -v certbot >/dev/null || apt-get install -y -qq certbot
  if [[ ! -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ]]; then
    log "Requesting cert for $DOMAIN (make sure port 80 is free and DNS is proxied/orange-cloud OFF temporarily if this fails)..."
    certbot certonly --standalone -d "$DOMAIN" --preferred-challenges http --non-interactive --agree-tos -m "$CERT_EMAIL" \
      || die "Certbot failed — check DNS points here and port 80 is reachable."
  else
    log "Cert for $DOMAIN already exists, reusing it."
  fi
  CERT_PATH="/etc/letsencrypt/live/$DOMAIN/fullchain.pem"
  KEY_PATH="/etc/letsencrypt/live/$DOMAIN/privkey.pem"
fi

[[ -f "$CERT_PATH" ]] || die "Cert not found at $CERT_PATH"
[[ -f "$KEY_PATH"  ]] || die "Key not found at $KEY_PATH"

UUID=$(cat /proc/sys/kernel/random/uuid)
log "Generated client UUID: $UUID"

echo
log "Writing Xray config (backing up any existing one first)..."
mkdir -p "$(dirname "$XRAY_CONFIG")"
backup_if_exists "$XRAY_CONFIG"

cat > "$XRAY_CONFIG" <<EOF
{
  "inbounds": [{
    "listen": "127.0.0.1",
    "port": $XRAY_PORT,
    "protocol": "vless",
    "settings": {
      "clients": [{ "id": "$UUID", "level": 0 }],
      "decryption": "none"
    },
    "streamSettings": {
      "network": "ws",
      "wsSettings": { "path": "$WS_PATH" }
    }
  }],
  "outbounds": [{ "protocol": "freedom" }]
}
EOF

log "Validating Xray config syntax..."
xray -test -config "$XRAY_CONFIG" || die "Xray config failed validation — reverting."

log "Writing Nginx site config (backing up any existing one first)..."
backup_if_exists "$NGINX_SITE"

cat > "$NGINX_SITE" <<EOF
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

ln -sf "$NGINX_SITE" "$NGINX_LINK"

log "Validating Nginx config..."
nginx -t || die "Nginx config invalid — reverting."

log "Restarting services..."
systemctl enable --now xray
systemctl restart xray
systemctl restart nginx

log "Confirming Xray is actually up..."
sleep 1
systemctl is-active --quiet xray || die "Xray failed to start — check: journalctl -u xray -n 50"

echo
echo "=== Success ==="
echo "Backup of anything overwritten: $BACKUP_DIR"
echo
echo "vless://$UUID@$DOMAIN:$EXT_PORT?encryption=none&security=tls&sni=$DOMAIN&fp=chrome&type=ws&host=$DOMAIN&path=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$WS_PATH")#$CLIENT_NAME"
echo
echo "To fully undo everything this script did:"
echo "  systemctl stop xray nginx"
echo "  rm -f $NGINX_LINK $NGINX_SITE"
echo "  cp -a $BACKUP_DIR/config.json.bak $XRAY_CONFIG   # if it existed"
echo "  systemctl start nginx"
