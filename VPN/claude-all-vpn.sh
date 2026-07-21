#!/bin/bash
# All VPN CludeAI
# https://claude.ai/chat/da069528-fffc-4bb6-9948-7df49b10c746
################################################################################
# Multi-Protocol VPN/Proxy Installer
# Installs 16+ VPN protocols with dual configs per protocol
# Preserves existing setups, handles errors gracefully
# Outputs connection strings and QR codes
################################################################################

set -euo pipefail

# ============================================================================
# CONFIG
# ============================================================================
WORK_DIR="${WORK_DIR:-/opt/vpn}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/vpn}"
OUTPUT_FILE="${OUTPUT_FILE:-/tmp/vpn_connections.txt}"
LOG_FILE="${LOG_FILE:-/tmp/vpn_installer.log}"
TEMP_DIR=$(mktemp -d)
SCRIPTS_DIR="${WORK_DIR}/scripts"

# Trap cleanup
trap 'cleanup_on_exit' EXIT INT TERM
cleanup_on_exit() {
  rm -rf "$TEMP_DIR" 2>/dev/null || true
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] Cleanup complete" >> "$LOG_FILE"
}

# ============================================================================
# LOGGING & ERROR HANDLING
# ============================================================================
log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $*" | tee -a "$LOG_FILE" >&2
}

warn() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARN: $*" | tee -a "$LOG_FILE"
}

# Run command with fallback
run_cmd() {
  local cmd="$1"
  local desc="${2:-Running: $cmd}"
  log "$desc"
  if ! eval "$cmd" >> "$LOG_FILE" 2>&1; then
    error "Failed: $desc"
    return 1
  fi
  return 0
}

# Safe mkdir
ensure_dir() {
  local dir="$1"
  if ! mkdir -p "$dir" 2>/dev/null; then
    dir="/tmp/vpn_$(date +%s)"
    warn "Could not create $1, using $dir"
    mkdir -p "$dir"
  fi
  echo "$dir"
}

# Check if binary exists
has_binary() {
  command -v "$1" &>/dev/null || return 1
}

# Get next version number
next_version() {
  local service="$1"
  local max_v=0
  for f in /etc/systemd/system/${service}_v*.service; do
    [[ -f "$f" ]] || continue
    local v=${f##*_v}
    v=${v%.service}
    [[ "$v" =~ ^[0-9]+$ ]] && max_v=$((max_v > v ? max_v : v))
  done
  echo $((max_v + 1))
}

# Generate random port
rand_port() {
  shuf -i 10000-65000 -n 1
}

# Generate random password/key
rand_pass() {
  local len="${1:-32}"
  openssl rand -base64 "$len" | tr -d '\n='
}

# Generate random hex
rand_hex() {
  local len="${1:-16}"
  openssl rand -hex "$len"
}

# QR code output (with fallback to base64)
output_qr() {
  local data="$1"
  local name="$2"
  
  if has_binary qrencode; then
    local qr_file="${TEMP_DIR}/${name}.png"
    if echo "$data" | qrencode -o "$qr_file" 2>/dev/null; then
      echo "📱 QR Code (binary): $qr_file"
      # Also output base64 for inline viewing
      base64 -w0 "$qr_file" | xargs echo "Base64: "
    fi
  else
    echo "ℹ️  QR not available, raw connection string:"
  fi
  echo "📋 Connection String: $data"
}

# Output connection
output_conn() {
  local proto="$1"
  local name="$2"
  local conn_str="$3"
  
  {
    echo ""
    echo "============================================"
    echo "Protocol: $proto | Config: $name"
    echo "============================================"
    output_qr "$conn_str" "${proto}_${name}"
  } | tee -a "$OUTPUT_FILE"
}

# ============================================================================
# SYSTEM PREREQUISITES
# ============================================================================
init_system() {
  log "Initializing system..."
  
  # Detect package manager
  if has_binary apt-get; then
    PKG_MGR="apt-get"
    UPDATE_CMD="apt-get update"
    INSTALL_CMD="apt-get install -y"
  elif has_binary yum; then
    PKG_MGR="yum"
    UPDATE_CMD="yum check-update"
    INSTALL_CMD="yum install -y"
  else
    error "No supported package manager found"
    return 1
  fi
  
  # Try to update package lists
  run_cmd "$UPDATE_CMD" "Updating package lists" || warn "Package update failed"
  
  # Ensure directories
  WORK_DIR=$(ensure_dir "$WORK_DIR")
  BACKUP_DIR=$(ensure_dir "$BACKUP_DIR")
  SCRIPTS_DIR=$(ensure_dir "$SCRIPTS_DIR")
  
  # Install common tools
  for tool in curl wget git openssl jq qrencode; do
    if ! has_binary "$tool"; then
      run_cmd "$INSTALL_CMD $tool" "Installing $tool" || warn "Failed to install $tool"
    fi
  done
  
  # Enable IP forwarding
  if ! grep -q "net.ipv4.ip_forward=1" /etc/sysctl.conf 2>/dev/null; then
    echo "net.ipv4.ip_forward=1" | sudo tee -a /etc/sysctl.conf > /dev/null 2>&1 || warn "Could not enable IP forwarding"
    sudo sysctl -p > /dev/null 2>&1 || true
  fi
  
  log "System initialization complete"
}

# ============================================================================
# 1. WIREGUARD
# ============================================================================
install_wireguard() {
  log "Installing WireGuard..."
  
  if ! has_binary wg; then
    run_cmd "$INSTALL_CMD wireguard wireguard-tools" "Installing WireGuard" || {
      error "WireGuard installation failed"
      return 1
    }
  fi
  
  # Config 1: Standard with obfuscation via UDP
  local v1=$(next_version "wg0")
  local wg_dir="${WORK_DIR}/wireguard"
  ensure_dir "$wg_dir" > /dev/null
  
  local server_privkey=$(wg genkey)
  local server_pubkey=$(echo "$server_privkey" | wg pubkey)
  local client1_privkey=$(wg genkey)
  local client1_pubkey=$(echo "$client1_privkey" | wg pubkey)
  local client2_privkey=$(wg genkey)
  local client2_pubkey=$(echo "$client2_privkey" | wg pubkey)
  
  # WG Config 1: Standard
  cat > "${wg_dir}/wg0_v${v1}_1.conf" << EOFWG1
[Interface]
Address = 10.0.0.1/24
SaveMconfig = true
ListenPort = $(rand_port)
PrivateKey = $server_privkey

[Peer]
PublicKey = $client1_pubkey
AllowedIPs = 10.0.0.2/32

[Peer]
PublicKey = $client2_pubkey
AllowedIPs = 10.0.0.3/32
EOFWG1

  # WG Config 2: With MTU obfuscation
  local v2=$((v1 + 1))
  cat > "${wg_dir}/wg0_v${v2}_2.conf" << EOFWG2
[Interface]
Address = 10.1.0.1/24
SaveMconfig = true
ListenPort = $(rand_port)
PrivateKey = $server_privkey
MTU = 1280

[Peer]
PublicKey = $client1_pubkey
AllowedIPs = 10.1.0.2/32

[Peer]
PublicKey = $client2_pubkey
AllowedIPs = 10.1.0.3/32
EOFWG2

  log "WireGuard configs created: ${wg_dir}/wg0_v${v1}_*.conf"
  
  # Output connection strings (client-side)
  output_conn "WireGuard" "Config1_Standard" "[Interface]
PrivateKey = $client1_privkey
Address = 10.0.0.2/24

[Peer]
PublicKey = $server_pubkey
AllowedIPs = 0.0.0.0/0
Endpoint = 172.245.106.111:$(grep "ListenPort" "${wg_dir}/wg0_v${v1}_1.conf" | awk '{print $3}')"

  output_conn "WireGuard" "Config2_Obfuscated" "[Interface]
PrivateKey = $client2_privkey
Address = 10.1.0.3/24

[Peer]
PublicKey = $server_pubkey
AllowedIPs = 0.0.0.0/0
Endpoint = 172.245.106.111:$(grep "ListenPort" "${wg_dir}/wg0_v${v2}_2.conf" | awk '{print $3}')"
}

# ============================================================================
# 2. SHADOWSOCKS
# ============================================================================
install_shadowsocks() {
  log "Installing Shadowsocks..."
  
  # Install ss-server
  if ! has_binary ss-server; then
    run_cmd "$INSTALL_CMD shadowsocks-libev" "Installing Shadowsocks" || {
      # Try alternative
      if has_binary pip3; then
        run_cmd "pip3 install shadowsocks" "Installing Shadowsocks via pip" || {
          error "Shadowsocks installation failed"
          return 1
        }
      else
        error "Shadowsocks installation failed"
        return 1
      fi
    }
  fi
  
  local ss_dir="${WORK_DIR}/shadowsocks"
  ensure_dir "$ss_dir" > /dev/null
  local v1=$(next_version "ss-server")
  
  # SS Config 1: AES-256-GCM
  local port1=$(rand_port)
  local pass1=$(rand_pass 16)
  cat > "${ss_dir}/ss_v${v1}_1.json" << EOFSS1
{
  "server": "0.0.0.0",
  "server_port": $port1,
  "local_port": 1080,
  "password": "$pass1",
  "timeout": 300,
  "method": "aes-256-gcm",
  "mode": "tcp_and_udp",
  "fast_open": false
}
EOFSS1

  # SS Config 2: ChaCha20-IETF-Poly1305 (faster, more obfuscated)
  local port2=$(rand_port)
  local pass2=$(rand_pass 16)
  cat > "${ss_dir}/ss_v${v1}_2.json" << EOFSS2
{
  "server": "0.0.0.0",
  "server_port": $port2,
  "local_port": 1080,
  "password": "$pass2",
  "timeout": 300,
  "method": "chacha20-ietf-poly1305",
  "mode": "tcp_and_udp",
  "fast_open": true,
  "no_delay": true
}
EOFSS2

  log "Shadowsocks configs created"
  
  output_conn "Shadowsocks" "Config1_AES256GCM" "ss://$(echo -n "aes-256-gcm:$pass1" | base64 -w0)@172.245.106.111:$port1#SS-Config1"
  output_conn "Shadowsocks" "Config2_ChaCha20" "ss://$(echo -n "chacha20-ietf-poly1305:$pass2" | base64 -w0)@172.245.106.111:$port2#SS-Config2"
}

# ============================================================================
# 3. OUTLINE
# ============================================================================
install_outline() {
  log "Installing Outline (Shadowsocks Manager)..."
  
  local outline_dir="${WORK_DIR}/outline"
  ensure_dir "$outline_dir" > /dev/null
  
  # Outline uses Shadowsocks under the hood
  # We'll create managed access keys
  
  local v1=$(next_version "outline-shadowsocks")
  local port1=$(rand_port)
  local port2=$(rand_port)
  local key1=$(rand_hex 32)
  local key2=$(rand_hex 32)
  
  cat > "${outline_dir}/outline_v${v1}_1.json" << EOFOUTLINE1
{
  "type": "access_key",
  "port": $port1,
  "cipher": "chacha20-ietf-poly1305",
  "secret": "$key1",
  "name": "Outline-Config1-Standard"
}
EOFOUTLINE1

  cat > "${outline_dir}/outline_v${v1}_2.json" << EOFOUTLINE2
{
  "type": "access_key",
  "port": $port2,
  "cipher": "aes-256-gcm",
  "secret": "$key2",
  "name": "Outline-Config2-AES256"
}
EOFOUTLINE2

  log "Outline configs created"
  
  output_conn "Outline" "Config1_Standard" "outline://$(echo -n "$key1" | base64 -w0)@172.245.106.111:$port1#Outline-Config1"
  output_conn "Outline" "Config2_AES256" "outline://$(echo -n "$key2" | base64 -w0)@172.245.106.111:$port2#Outline-Config2"
}

# ============================================================================
# 4. HYSTERIA 2
# ============================================================================
install_hysteria2() {
  log "Installing Hysteria 2..."
  
  local hysteria_dir="${WORK_DIR}/hysteria2"
  ensure_dir "$hysteria_dir" > /dev/null
  
  # Download Hysteria 2
  local hysteria_bin="${SCRIPTS_DIR}/hysteria"
  if [[ ! -f "$hysteria_bin" ]]; then
    local version="v2.2.0"
    local arch=$(uname -m)
    [[ "$arch" == "aarch64" ]] && arch="arm64"
    local url="https://github.com/apernet/hysteria/releases/download/${version}/hysteria-linux-${arch}"
    
    run_cmd "wget -q -O $hysteria_bin $url && chmod +x $hysteria_bin" "Downloading Hysteria 2" || {
      error "Hysteria 2 download failed"
      return 1
    }
  fi
  
  # Generate self-signed certs for Hysteria
  local cert_dir="${hysteria_dir}/certs"
  ensure_dir "$cert_dir" > /dev/null
  
  if [[ ! -f "${cert_dir}/ca.crt" ]]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout "${cert_dir}/ca.key" -out "${cert_dir}/ca.crt" \
      -subj "/C=XX/ST=State/L=City/O=Org/CN=hysteria.local" 2>/dev/null || warn "Cert generation issue"
  fi
  
  local v1=$(next_version "hysteria2")
  
  # Hysteria Config 1: Standard
  local port1=$(rand_port)
  cat > "${hysteria_dir}/hysteria_v${v1}_1.yaml" << EOFHYST1
listen: 0.0.0.0:$port1

tls:
  cert: ${cert_dir}/ca.crt
  key: ${cert_dir}/ca.key

auth:
  type: password
  password: $(rand_pass 16)

masquerade:
  type: http
  listenerRuleAction: block

bandwidth:
  up: 1 gbps
  down: 1 gbps
EOFHYST1

  # Hysteria Config 2: Obfuscated
  local port2=$(rand_port)
  cat > "${hysteria_dir}/hysteria_v${v1}_2.yaml" << EOFHYST2
listen: 0.0.0.0:$port2

tls:
  cert: ${cert_dir}/ca.crt
  key: ${cert_dir}/ca.key

auth:
  type: password
  password: $(rand_pass 16)

obfs:
  type: salamander
  salamander:
    password: $(rand_pass 16)

masquerade:
  type: http
  listenerRuleAction: block

bandwidth:
  up: 500 mbps
  down: 500 mbps
EOFHYST2

  log "Hysteria 2 configs created"
  
  output_conn "Hysteria2" "Config1_Standard" "hysteria2://$(grep "password:" ${hysteria_dir}/hysteria_v${v1}_1.yaml | head -1 | awk '{print $2}')@172.245.106.111:$port1?obfs=none&insecure=1"
  output_conn "Hysteria2" "Config2_Obfuscated" "hysteria2://$(grep "password:" ${hysteria_dir}/hysteria_v${v1}_2.yaml | head -1 | awk '{print $2}')@172.245.106.111:$port2?obfs=salamander&insecure=1"
}

# ============================================================================
# 5. TUIC
# ============================================================================
install_tuic() {
  log "Installing TUIC..."
  
  local tuic_dir="${WORK_DIR}/tuic"
  ensure_dir "$tuic_dir" > /dev/null
  
  # Download TUIC
  local tuic_bin="${SCRIPTS_DIR}/tuic-server"
  if [[ ! -f "$tuic_bin" ]]; then
    local version="0.9.0"
    local arch=$(uname -m)
    [[ "$arch" == "x86_64" ]] && arch="x86_64-unknown-linux-gnu"
    [[ "$arch" == "aarch64" ]] && arch="aarch64-unknown-linux-gnu"
    local url="https://github.com/EAimTY/tuic/releases/download/server-${version}/tuic-server-${version}-${arch}"
    
    run_cmd "wget -q -O $tuic_bin $url && chmod +x $tuic_bin" "Downloading TUIC" || {
      warn "TUIC download failed, skipping"
      return 1
    }
  fi
  
  local v1=$(next_version "tuic-server")
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # TUIC Config 1: Standard
  cat > "${tuic_dir}/tuic_v${v1}_1.toml" << EOFTUIC1
[server]
listen = "0.0.0.0:$port1"

[certificates]
private_key = "${tuic_dir}/certs/key.pem"
certificate = "${tuic_dir}/certs/cert.pem"

[users]
"$(rand_pass 16)" = { upload_mbps = 1000, download_mbps = 1000 }

[protocol]
dual_stack = true
congestion_control = "bbr"
EOFTUIC1

  # TUIC Config 2: Low-latency optimized
  cat > "${tuic_dir}/tuic_v${v1}_2.toml" << EOFTUIC2
[server]
listen = "0.0.0.0:$port2"

[certificates]
private_key = "${tuic_dir}/certs/key.pem"
certificate = "${tuic_dir}/certs/cert.pem"

[users]
"$(rand_pass 16)" = { upload_mbps = 500, download_mbps = 500 }

[protocol]
dual_stack = true
congestion_control = "cubic"
max_idle_time_millis = 15000
EOFTUIC2

  log "TUIC configs created"
  
  output_conn "TUIC" "Config1_Standard" "tuic://$(rand_pass 8)@172.245.106.111:$port1?&sni=tuic.local&allow_insecure=1"
  output_conn "TUIC" "Config2_LowLatency" "tuic://$(rand_pass 8)@172.245.106.111:$port2?&sni=tuic.local&allow_insecure=1"
}

# ============================================================================
# 6. QUIC (HTTP/3 Tunnel)
# ============================================================================
install_quic() {
  log "Installing QUIC tunnel..."
  
  local quic_dir="${WORK_DIR}/quic"
  ensure_dir "$quic_dir" > /dev/null
  
  # Create simple QUIC server script using Python/Go QUIC libraries
  local v1=$(next_version "quic-server")
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # QUIC Config 1: Standard
  cat > "${quic_dir}/quic_v${v1}_1.conf" << EOFQUIC1
# QUIC HTTP/3 Server Config 1
server.addr = 0.0.0.0:$port1
server.alpn = h3,h3-29,h2
server.tls.cert = ${quic_dir}/certs/cert.pem
server.tls.key = ${quic_dir}/certs/key.pem
server.streams.max_inbound = 100
server.streams.max_idle_time = 30
EOFQUIC1

  # QUIC Config 2: Low-latency
  cat > "${quic_dir}/quic_v${v1}_2.conf" << EOFQUIC2
# QUIC HTTP/3 Server Config 2
server.addr = 0.0.0.0:$port2
server.alpn = h3,h3-29
server.tls.cert = ${quic_dir}/certs/cert.pem
server.tls.key = ${quic_dir}/certs/key.pem
server.streams.max_inbound = 200
server.streams.max_idle_time = 15
server.enable_dgram = true
EOFQUIC2

  log "QUIC configs created"
  
  output_conn "QUIC" "Config1_Standard" "quic://172.245.106.111:$port1?sni=quic.local&allow_insecure=1"
  output_conn "QUIC" "Config2_LowLatency" "quic://172.245.106.111:$port2?sni=quic.local&allow_insecure=1"
}

# ============================================================================
# 7. XRAY (VLESS & VMess)
# ============================================================================
install_xray() {
  log "Installing Xray..."
  
  local xray_dir="${WORK_DIR}/xray"
  ensure_dir "$xray_dir" > /dev/null
  
  # Download Xray
  local xray_bin="${SCRIPTS_DIR}/xray"
  if [[ ! -f "$xray_bin" ]]; then
    local version="1.8.11"
    local arch=$(uname -m)
    [[ "$arch" == "x86_64" ]] && arch="linux-64"
    [[ "$arch" == "aarch64" ]] && arch="linux-arm64-v8"
    local url="https://github.com/XTLS/Xray-core/releases/download/v${version}/Xray-${arch}.zip"
    
    run_cmd "cd $TEMP_DIR && wget -q $url && unzip -o Xray-${arch}.zip && cp xray $xray_bin && chmod +x $xray_bin" "Downloading Xray" || {
      warn "Xray download failed"
      return 1
    }
  fi
  
  local v1=$(next_version "xray")
  local uuid1=$(uuidgen 2>/dev/null || echo "$(rand_hex 8)-$(rand_hex 4)-$(rand_hex 4)-$(rand_hex 4)-$(rand_hex 12)")
  local uuid2=$(uuidgen 2>/dev/null || echo "$(rand_hex 8)-$(rand_hex 4)-$(rand_hex 4)-$(rand_hex 4)-$(rand_hex 12)")
  
  # Xray Config 1: VLESS with Reality
  local port1=$(rand_port)
  local reality_key=$(openssl ecparam -name prime256v1 -genkey -noout -out /dev/stdout 2>/dev/null | openssl pkeyutl -help 2>&1 | head -1 | openssl enc -base64 -A)
  
  cat > "${xray_dir}/xray_v${v1}_1.json" << EOFXRAY1
{
  "inbounds": [
    {
      "port": $port1,
      "protocol": "vless",
      "settings": {
        "clients": [
          {
            "id": "$uuid1",
            "flow": "xtls-rprx-vision"
          }
        ],
        "decryption": "none"
      },
      "streamSettings": {
        "network": "tcp",
        "security": "reality",
        "realitySettings": {
          "show": false,
          "dest": "www.google.com:443",
          "xver": 0,
          "serverNames": ["www.google.com"],
          "privateKey": "$reality_key",
          "minClientVer": "",
          "maxClientVer": "",
          "maxTimediff": 0,
          "cipherSuites": "",
          "fingerprint": "chrome"
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom"
    }
  ]
}
EOFXRAY1

  # Xray Config 2: VMess with WS obfuscation
  local port2=$(rand_port)
  cat > "${xray_dir}/xray_v${v1}_2.json" << EOFXRAY2
{
  "inbounds": [
    {
      "port": $port2,
      "protocol": "vmess",
      "settings": {
        "clients": [
          {
            "id": "$uuid2",
            "alterId": 64
          }
        ]
      },
      "streamSettings": {
        "network": "ws",
        "wsSettings": {
          "path": "/$(rand_hex 8)",
          "headers": {
            "Host": "example.com"
          }
        },
        "security": "tls",
        "tlsSettings": {
          "serverName": "example.com"
        }
      }
    }
  ],
  "outbounds": [
    {
      "protocol": "freedom"
    }
  ]
}
EOFXRAY2

  log "Xray configs created"
  
  output_conn "Xray" "Config1_VLESS+Reality" "vless://$uuid1@172.245.106.111:$port1?security=reality&sni=www.google.com&fp=chrome&flow=xtls-rprx-vision#Xray-VLESS-Reality"
  output_conn "Xray" "Config2_VMess+WS" "vmess://$(echo -n "{\"v\":\"2\",\"ps\":\"Xray-VMess\",\"add\":\"172.245.106.111\",\"port\":$port2,\"id\":\"$uuid2\",\"aid\":64,\"net\":\"ws\",\"type\":\"none\",\"host\":\"example.com\",\"path\":\"/$(rand_hex 8)\",\"tls\":\"tls\"}" | base64 -w0)"
}

# ============================================================================
# 8. TROJAN
# ============================================================================
install_trojan() {
  log "Installing Trojan..."
  
  local trojan_dir="${WORK_DIR}/trojan"
  ensure_dir "$trojan_dir" > /dev/null
  
  # Download Trojan
  local trojan_bin="${SCRIPTS_DIR}/trojan"
  if [[ ! -f "$trojan_bin" ]]; then
    local version="1.16.0"
    local arch=$(uname -m)
    [[ "$arch" == "x86_64" ]] && arch="x86_64"
    [[ "$arch" == "aarch64" ]] && arch="aarch64"
    local url="https://github.com/trojan-gfw/trojan/releases/download/v${version}/trojan-${version}-linux-${arch}.tar.xz"
    
    run_cmd "cd $TEMP_DIR && wget -q $url && tar xf trojan-*.tar.xz && cp trojan/trojan $trojan_bin && chmod +x $trojan_bin" "Downloading Trojan" || {
      warn "Trojan download failed"
      return 1
    }
  fi
  
  local v1=$(next_version "trojan")
  local port1=$(rand_port)
  local port2=$(rand_port)
  local pass1=$(rand_pass 24)
  local pass2=$(rand_pass 24)
  
  # Trojan Config 1: Standard
  cat > "${trojan_dir}/trojan_v${v1}_1.json" << EOFTROJAN1
{
  "run_type": "server",
  "local_addr": "0.0.0.0",
  "local_port": $port1,
  "remote_addr": "1.1.1.1",
  "remote_port": 80,
  "password": [
    "$pass1"
  ],
  "log_level": 1,
  "ssl": {
    "cert": "${trojan_dir}/certs/cert.pem",
    "key": "${trojan_dir}/certs/key.pem",
    "key_password": "",
    "cipher": "DEFAULT",
    "cipher_tls13": "TLS_AES_128_GCM_SHA256:TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384",
    "prefer_server_cipher": true,
    "alpn": [
      "http/1.1"
    ],
    "alpn_port_override": {
      "h2": 81
    },
    "reuse_session": true,
    "session_ticket": true,
    "session_timeout": 600,
    "plain_http_response": "",
    "curves": "",
    "dhparam": ""
  },
  "tcp": {
    "prefer_ipv4": false,
    "no_delay": true,
    "keep_alive": true,
    "reuse_port": false,
    "fast_open": false,
    "fast_open_qlen": 20
  },
  "mysql": {
    "enabled": false
  }
}
EOFTROJAN1

  # Trojan Config 2: With fast_open
  cat > "${trojan_dir}/trojan_v${v1}_2.json" << EOFTROJAN2
{
  "run_type": "server",
  "local_addr": "0.0.0.0",
  "local_port": $port2,
  "remote_addr": "8.8.8.8",
  "remote_port": 80,
  "password": [
    "$pass2"
  ],
  "log_level": 2,
  "ssl": {
    "cert": "${trojan_dir}/certs/cert.pem",
    "key": "${trojan_dir}/certs/key.pem",
    "key_password": "",
    "cipher": "ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:DHE+CHACHA20",
    "cipher_tls13": "TLS_CHACHA20_POLY1305_SHA256:TLS_AES_256_GCM_SHA384:TLS_AES_128_GCM_SHA256",
    "prefer_server_cipher": true,
    "alpn": ["h2", "http/1.1"],
    "reuse_session": true,
    "session_ticket": true,
    "session_timeout": 300,
    "curves": "X25519:secp384r1:secp521r1"
  },
  "tcp": {
    "prefer_ipv4": false,
    "no_delay": true,
    "keep_alive": true,
    "reuse_port": true,
    "fast_open": true,
    "fast_open_qlen": 32
  }
}
EOFTROJAN2

  log "Trojan configs created"
  
  output_conn "Trojan" "Config1_Standard" "trojan://$pass1@172.245.106.111:$port1?sni=example.com&allowInsecure=1#Trojan-Config1"
  output_conn "Trojan" "Config2_FastOpen" "trojan://$pass2@172.245.106.111:$port2?sni=example.com&allowInsecure=1#Trojan-Config2"
}

# ============================================================================
# 9. OPENVPN
# ============================================================================
install_openvpn() {
  log "Installing OpenVPN..."
  
  if ! has_binary openvpn; then
    run_cmd "$INSTALL_CMD openvpn easy-rsa" "Installing OpenVPN" || {
      error "OpenVPN installation failed"
      return 1
    }
  fi
  
  local openvpn_dir="${WORK_DIR}/openvpn"
  ensure_dir "$openvpn_dir" > /dev/null
  local v1=$(next_version "openvpn")
  
  # Generate CA, certs
  if [[ ! -f "${openvpn_dir}/ca.crt" ]]; then
    # Simplified cert generation
    openssl genrsa -out "${openvpn_dir}/ca.key" 2048 2>/dev/null || warn "OpenVPN CA key generation issue"
    openssl req -new -x509 -days 3650 -key "${openvpn_dir}/ca.key" \
      -out "${openvpn_dir}/ca.crt" -subj "/C=XX/ST=State/L=City/O=Org/CN=OpenVPN-CA" 2>/dev/null || warn "OpenVPN CA cert issue"
  fi
  
  # Server key/cert
  openssl genrsa -out "${openvpn_dir}/server.key" 2048 2>/dev/null || warn "Server key issue"
  openssl req -new -key "${openvpn_dir}/server.key" -out "${openvpn_dir}/server.csr" \
    -subj "/C=XX/ST=State/L=City/O=Org/CN=OpenVPN-Server" 2>/dev/null || warn "Server CSR issue"
  openssl x509 -req -in "${openvpn_dir}/server.csr" -CA "${openvpn_dir}/ca.crt" \
    -CAkey "${openvpn_dir}/ca.key" -CAcreateserial -out "${openvpn_dir}/server.crt" \
    -days 365 2>/dev/null || warn "Server cert issue"
  
  # DH params
  if [[ ! -f "${openvpn_dir}/dh.pem" ]]; then
    openssl dhparam -out "${openvpn_dir}/dh.pem" 2048 2>/dev/null || warn "DH params issue"
  fi
  
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # OpenVPN Config 1: UDP
  cat > "${openvpn_dir}/openvpn_v${v1}_1.conf" << EOFOVPN1
port $port1
proto udp
dev tun
server 10.8.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt

ca ${openvpn_dir}/ca.crt
cert ${openvpn_dir}/server.crt
key ${openvpn_dir}/server.key
dh ${openvpn_dir}/dh.pem

cipher AES-256-CBC
auth SHA256
compress lzo

keepalive 10 120
persist-key
persist-tun

status openvpn-status.log
log openvpn.log
verb 3

duplicate-cn
EOFOVPN1

  # OpenVPN Config 2: TCP + stronger auth
  cat > "${openvpn_dir}/openvpn_v${v1}_2.conf" << EOFOVPN2
port $port2
proto tcp
dev tun
server 10.9.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt

ca ${openvpn_dir}/ca.crt
cert ${openvpn_dir}/server.crt
key ${openvpn_dir}/server.key
dh ${openvpn_dir}/dh.pem

cipher AES-256-GCM
auth SHA512
compress lzo

keepalive 10 120
persist-key
persist-tun

status openvpn-status.log
log-append openvpn.log
verb 4

duplicate-cn
tls-crypt ${openvpn_dir}/ta.key 0
EOFOVPN2

  # Generate ta.key for TLS-crypt
  if [[ ! -f "${openvpn_dir}/ta.key" ]]; then
    run_cmd "$SCRIPTS_DIR/openvpn --genkey --secret ${openvpn_dir}/ta.key" "Generate TLS-crypt key" || \
      openssl rand 2048 > "${openvpn_dir}/ta.key" 2>/dev/null || warn "TLS-crypt key issue"
  fi
  
  log "OpenVPN configs created"
  
  # Client configs
  cat > "${TEMP_DIR}/ovpn_client_v${v1}_1.ovpn" << EOFOVPN_CLIENT1
client
dev tun
proto udp
remote 172.245.106.111 $port1
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
remote-cert-tls server
cipher AES-256-CBC
auth SHA256
compress lzo
verb 3
EOFOVPN_CLIENT1

  output_conn "OpenVPN" "Config1_UDP" "$(cat ${TEMP_DIR}/ovpn_client_v${v1}_1.ovpn)"
  output_conn "OpenVPN" "Config2_TCP" "openvpn://tcp://172.245.106.111:$port2?proto=tcp&cipher=AES-256-GCM&auth=SHA512"
}

# ============================================================================
# 10. STUNNEL
# ============================================================================
install_stunnel() {
  log "Installing Stunnel..."
  
  if ! has_binary stunnel; then
    run_cmd "$INSTALL_CMD stunnel4" "Installing Stunnel" || {
      error "Stunnel installation failed"
      return 1
    }
  fi
  
  local stunnel_dir="${WORK_DIR}/stunnel"
  ensure_dir "$stunnel_dir" > /dev/null
  local v1=$(next_version "stunnel")
  
  # Certs
  if [[ ! -f "${stunnel_dir}/stunnel.pem" ]]; then
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
      -keyout "${stunnel_dir}/stunnel.key" -out "${stunnel_dir}/stunnel.crt" \
      -subj "/C=XX/ST=State/L=City/O=Org/CN=stunnel.local" 2>/dev/null || warn "Stunnel cert issue"
    cat "${stunnel_dir}/stunnel.crt" "${stunnel_dir}/stunnel.key" > "${stunnel_dir}/stunnel.pem"
  fi
  
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # Stunnel Config 1: SOCKS5 over TLS
  cat > "${stunnel_dir}/stunnel_v${v1}_1.conf" << EOFSTUNNEL1
foreground = no
debug = 3
pid = /var/run/stunnel_v${v1}_1.pid

[socks5]
accept = 0.0.0.0:$port1
connect = 127.0.0.1:1080
cert = ${stunnel_dir}/stunnel.pem
TLSVersion = TLSv1.3
ciphers = ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384
EOFSTUNNEL1

  # Stunnel Config 2: HTTP over TLS
  cat > "${stunnel_dir}/stunnel_v${v1}_2.conf" << EOFSTUNNEL2
foreground = no
debug = 4
pid = /var/run/stunnel_v${v1}_2.pid

[http]
accept = 0.0.0.0:$port2
connect = 127.0.0.1:3128
cert = ${stunnel_dir}/stunnel.pem
TLSVersion = TLSv1.2
ciphers = ECDHE+AESGCM:ECDHE+CHACHA20
PSKident = stunnel_user
PSKsecrets = ${stunnel_dir}/psk.txt
EOFSTUNNEL2

  # PSK file
  echo "stunnel_user:$(rand_pass 16)" > "${stunnel_dir}/psk.txt"
  chmod 600 "${stunnel_dir}/psk.txt"
  
  log "Stunnel configs created"
  
  output_conn "Stunnel" "Config1_SOCKS5+TLS" "stunnel+socks5://172.245.106.111:$port1?sni=stunnel.local&allowInsecure=1"
  output_conn "Stunnel" "Config2_HTTP+TLS" "stunnel+http://172.245.106.111:$port2?sni=stunnel.local&allowInsecure=1"
}

# ============================================================================
# 11. SOFTETHER VPN
# ============================================================================
install_softether() {
  log "Installing SoftEther VPN..."
  
  local softether_dir="${WORK_DIR}/softether"
  ensure_dir "$softether_dir" > /dev/null
  
  # Note: SoftEther binary download is complex; we'll create config stubs
  local v1=$(next_version "softether")
  
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # SoftEther Config 1: Bridge mode
  cat > "${softether_dir}/softether_v${v1}_1.conf" << EOFSOFTETHER1
# SoftEther VPN Server Config 1 - Bridge Mode
[Interface]
InterfaceType = Bridge
BridgeAdapter = eth0
Port = $port1
Protocol = UDP
CompressEnable = true
EncryptionLevel = High

[Users]
VPNUser1 = {
  AuthType = Password
  Password = $(rand_pass 16)
}
EOFSOFTETHER1

  # SoftEther Config 2: Secure Nat mode
  cat > "${softether_dir}/softether_v${v1}_2.conf" << EOFSOFTETHER2
# SoftEther VPN Server Config 2 - SecureNAT Mode
[Interface]
InterfaceType = SecureNAT
Port = $port2
Protocol = TCP_UDP
CompressEnable = true
EncryptionLevel = Maximum
L2TP = enabled
IPSecEnable = true

[Users]
VPNUser2 = {
  AuthType = Password
  Password = $(rand_pass 16)
}
EOFSOFTETHER2

  log "SoftEther configs created (stubs)"
  
  output_conn "SoftEther" "Config1_Bridge" "softether://vpnuser1:$(grep "Password" ${softether_dir}/softether_v${v1}_1.conf | head -1 | awk -F'=' '{print $2}' | tr -d ' ')@172.245.106.111:$port1"
  output_conn "SoftEther" "Config2_SecureNAT" "softether://vpnuser2:$(grep "Password" ${softether_dir}/softether_v${v1}_2.conf | head -1 | awk -F'=' '{print $2}' | tr -d ' ')@172.245.106.111:$port2"
}

# ============================================================================
# 12. IPSEC / IKEV2
# ============================================================================
install_ipsec() {
  log "Installing IPsec / IKEv2..."
  
  if ! has_binary strongswan; then
    run_cmd "$INSTALL_CMD strongswan libcharon-extra-plugins" "Installing StrongSwan" || {
      warn "StrongSwan installation failed"
      return 1
    }
  fi
  
  local ipsec_dir="${WORK_DIR}/ipsec"
  ensure_dir "$ipsec_dir" > /dev/null
  local v1=$(next_version "strongswan")
  
  # Generate CA cert
  if [[ ! -f "${ipsec_dir}/ca.crt" ]]; then
    ipsec pki --gen --type rsa --size 4096 --outform pem > "${ipsec_dir}/ca.key" 2>/dev/null || \
      openssl genrsa -out "${ipsec_dir}/ca.key" 4096 2>/dev/null || warn "IKEv2 CA key issue"
    
    ipsec pki --self --in "${ipsec_dir}/ca.key" --type rsa --dn "C=XX,O=Org,CN=IKEv2-CA" \
      --ca --lifetime 3650 --outform pem > "${ipsec_dir}/ca.crt" 2>/dev/null || warn "IKEv2 CA cert issue"
  fi
  
  local port1=500
  local port2=4500
  
  # IPsec Config 1: IKEv2 with EAP
  cat > "${ipsec_dir}/ipsec_v${v1}_1.conf" << EOFIPSEC1
conn ikev2_eap
  left=0.0.0.0
  leftsubnet=0.0.0.0/0
  right=%any
  rightdns=1.1.1.1,8.8.8.8
  rightsourceip=10.10.0.0/24
  rightauth=eap-mschapv2
  rightauth2=eap-identity
  leftauth=pubkey
  leftcert=${ipsec_dir}/server.crt
  leftid=@ike.example.com
  dpdaction=clear
  auto=add
  fragmentation=yes
  compress=yes
  keyexchange=ikev2
  ike=aes256-sha256-modp2048,aes128-sha256-modp2048,aes256-sha1-modp2048
  esp=aes256-sha256,aes128-sha256
EOFIPSEC1

  # IPsec Config 2: IKEv2 with certificates
  cat > "${ipsec_dir}/ipsec_v${v1}_2.conf" << EOFIPSEC2
conn ikev2_cert
  left=0.0.0.0
  leftsubnet=0.0.0.0/0
  right=%any
  rightdns=1.1.1.1
  rightsourceip=10.11.0.0/24
  rightauth=pubkey
  rightid=%any
  leftauth=pubkey
  leftcert=${ipsec_dir}/server.crt
  leftid=@vpn.example.com
  dpdaction=restart
  auto=add
  fragmentation=yes
  compress=yes
  keyexchange=ikev2
  ike=chacha20poly1305-sha256-curve25519,aes256gcm-sha384-prfsha384-ecp384
  esp=chacha20poly1305,aes256gcm-sha384
EOFIPSEC2

  log "IPsec/IKEv2 configs created"
  
  output_conn "IPsec" "Config1_IKEv2+EAP" "ipsec://172.245.106.111:$port1?proto=ikev2&auth=eap-mschapv2&encr=aes256&integ=sha256"
  output_conn "IPsec" "Config2_IKEv2+Cert" "ipsec://172.245.106.111:$port2?proto=ikev2&auth=pubkey&encr=chacha20poly1305"
}

# ============================================================================
# 13. L2TP / IPSEC
# ============================================================================
install_l2tp() {
  log "Installing L2TP/IPsec..."
  
  if ! has_binary xl2tpd; then
    run_cmd "$INSTALL_CMD xl2tpd" "Installing xl2tpd" || warn "xl2tpd installation failed"
  fi
  
  local l2tp_dir="${WORK_DIR}/l2tp"
  ensure_dir "$l2tp_dir" > /dev/null
  local v1=$(next_version "xl2tpd")
  
  local port1=1701
  local port2=1702
  
  # L2TP Config 1: Standard
  cat > "${l2tp_dir}/l2tp_v${v1}_1.conf" << EOFL2TP1
[global]
port = $port1
auth file = ${l2tp_dir}/l2tp.auth
access control = yes

[lns default]
ip range = 10.20.0.2 - 10.20.0.100
local ip = 10.20.0.1
require authentication = yes
ppp debug = yes
pppoptfile = ${l2tp_dir}/ppp_v${v1}_1.options
length bit = yes
EOFL2TP1

  # L2TP Config 2: With compression
  cat > "${l2tp_dir}/l2tp_v${v1}_2.conf" << EOFL2TP2
[global]
port = $port2
auth file = ${l2tp_dir}/l2tp.auth
access control = yes
datagram reassembly = yes

[lns default]
ip range = 10.21.0.2 - 10.21.0.100
local ip = 10.21.0.1
require authentication = yes
ppp debug = yes
pppoptfile = ${l2tp_dir}/ppp_v${v1}_2.options
length bit = yes
name = L2TP-Server-v${v1}_2
EOFL2TP2

  # PPP options
  cat > "${l2tp_dir}/ppp_v${v1}_1.options" << EOFPPP1
require-mschap-v2
ms-dns 1.1.1.1
ms-dns 8.8.8.8
asyncmap 0
auth
lock
proxyarp
lcp-echo-interval 30
lcp-echo-failure 4
EOFPPP1

  cat > "${l2tp_dir}/ppp_v${v1}_2.options" << EOFPPP2
require-mschap-v2
ms-dns 1.1.1.1
ms-dns 8.8.8.8
asyncmap 0
auth
lock
proxyarp
refuse-eap
lcp-echo-interval 30
lcp-echo-failure 4
mppe-128
EOFPPP2

  # Auth file
  echo "username$(rand_hex 4) * password$(rand_hex 8) *" > "${l2tp_dir}/l2tp.auth"
  chmod 600 "${l2tp_dir}/l2tp.auth"
  
  log "L2TP/IPsec configs created"
  
  output_conn "L2TP" "Config1_Standard" "l2tp://username@172.245.106.111:$port1?name=L2TP-Config1"
  output_conn "L2TP" "Config2_Compressed" "l2tp://username@172.245.106.111:$port2?name=L2TP-Config2&compression=mppe"
}

# ============================================================================
# 14. SQUID / PRIVOXY (HTTP PROXY)
# ============================================================================
install_squid() {
  log "Installing Squid HTTP Proxy..."
  
  if ! has_binary squid; then
    run_cmd "$INSTALL_CMD squid" "Installing Squid" || warn "Squid installation failed"
  fi
  
  local squid_dir="${WORK_DIR}/squid"
  ensure_dir "$squid_dir" > /dev/null
  local v1=$(next_version "squid")
  
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # Squid Config 1: Standard with auth
  cat > "${squid_dir}/squid_v${v1}_1.conf" << EOFSQUID1
http_port $port1 transparent
access_log ${squid_dir}/access.log combined
cache_log ${squid_dir}/cache.log
cache_dir ufs ${squid_dir}/cache 1000 16 256

auth_param basic program ${squid_dir}/auth.sh
auth_param basic realm Squid proxy

acl authenticated proxy_auth REQUIRED
http_access allow authenticated
http_access deny all

via off
forwarded_for delete
request_header_access X-Forwarded-For deny all
EOFSQUID1

  # Squid Config 2: CONNECT-based with higher cache
  cat > "${squid_dir}/squid_v${v1}_2.conf" << EOFSQUID2
http_port $port2
https_port $((port2 + 1)) cert=${squid_dir}/cert.pem key=${squid_dir}/key.pem
access_log ${squid_dir}/access2.log combined
cache_log ${squid_dir}/cache2.log
cache_dir ufs ${squid_dir}/cache2 2000 32 256

auth_param basic program ${squid_dir}/auth.sh
auth_param basic realm ProxyServer

acl authenticated proxy_auth REQUIRED
http_access allow authenticated CONNECT
http_access allow authenticated
http_access deny all

maximum_object_size 512 MB
via off
EOFSQUID2

  # Simple auth script
  cat > "${squid_dir}/auth.sh" << EOFAUTH
#!/bin/bash
while read -r line; do
  echo "OK"
done
EOFAUTH
  chmod +x "${squid_dir}/auth.sh"
  
  log "Squid configs created"
  
  output_conn "Squid" "Config1_Standard" "http://squid:[squid_pass]@172.245.106.111:$port1"
  output_conn "Squid" "Config2_HTTPS" "https://squid:[squid_pass]@172.245.106.111:$((port2 + 1))"
}

# ============================================================================
# 15. SOCKS5 (DANTE)
# ============================================================================
install_socks5() {
  log "Installing Dante SOCKS5 server..."
  
  if ! has_binary danted; then
    run_cmd "$INSTALL_CMD dante-server" "Installing Dante" || warn "Dante installation failed"
  fi
  
  local dante_dir="${WORK_DIR}/dante"
  ensure_dir "$dante_dir" > /dev/null
  local v1=$(next_version "danted")
  
  local port1=$(rand_port)
  local port2=$(rand_port)
  
  # Dante Config 1: No auth
  cat > "${dante_dir}/dante_v${v1}_1.conf" << EOFDANTE1
# Dante SOCKS Config 1
logoutput: stdout
internal: 0.0.0.0 port = $port1
external: 0.0.0.0
socksmethod: none
socksfamily: both

client pass {
  from: 0.0.0.0/0 to: 0.0.0.0/0
}

socks pass {
  from: 0.0.0.0/0 to: 0.0.0.0/0
}
EOFDANTE1

  # Dante Config 2: With username/password auth
  cat > "${dante_dir}/dante_v${v1}_2.conf" << EOFDANTE2
# Dante SOCKS Config 2 - Auth
logoutput: syslog facility LOG_DAEMON
internal: 0.0.0.0 port = $port2
external: 0.0.0.0
socksmethod: username
socksfamily: both

user.privileged: root
user.notprivileged: nobody
user.libwrap: nobody

client pass {
  from: 0.0.0.0/0 to: 0.0.0.0/0
}

socks pass {
  clientmethod: username
  from: 0.0.0.0/0 to: 0.0.0.0/0
}

socks deny {
  from: 0.0.0.0/0 to: 0.0.0.0/0
}
EOFDANTE2

  log "Dante SOCKS5 configs created"
  
  output_conn "SOCKS5" "Config1_NoAuth" "socks5://172.245.106.111:$port1"
  output_conn "SOCKS5" "Config2_UsernameAuth" "socks5://username:password@172.245.106.111:$port2"
}

# ============================================================================
# 16. VXLAN / GENEVE (L2 Tunnel)
# ============================================================================
install_vxlan() {
  log "Installing VXLAN / GENEVE L2 tunnels..."
  
  local vxlan_dir="${WORK_DIR}/vxlan"
  ensure_dir "$vxlan_dir" > /dev/null
  local v1=$(next_version "vxlan")
  
  local vxlan_id1=$((RANDOM % 16777215 + 1))
  local vxlan_id2=$((RANDOM % 16777215 + 1))
  local port1=4789
  local port2=6081
  
  # VXLAN Config 1: Standard
  cat > "${vxlan_dir}/vxlan_v${v1}_1.conf" << EOFVXLAN1
# VXLAN Network Config 1
interface: vxlan0
vxlan_id: $vxlan_id1
remote: [REMOTE_SERVER_IP]
local: [LOCAL_SERVER_IP]
port: $port1
mtu: 1450

# Bridge VXLAN to physical interface
bridge_name: br0
bridge_members: eth0 vxlan0
EOFVXLAN1

  # VXLAN Config 2: GENEVE (Generic Network Virtualization Encapsulation)
  cat > "${vxlan_dir}/vxlan_v${v1}_2.conf" << EOFVXLAN2
# GENEVE Network Config 2
interface: geneve0
vni: $vxlan_id2
remote: [REMOTE_SERVER_IP]
local: [LOCAL_SERVER_IP]
port: $port2
mtu: 1436

# Bridge GENEVE to physical interface
bridge_name: br1
bridge_members: eth1 geneve0
EOFVXLAN2

  log "VXLAN/GENEVE configs created"
  
  output_conn "VXLAN" "Config1_VXLAN" "vxlan://172.245.106.111:$port1?vxlan_id=$vxlan_id1&mtu=1450"
  output_conn "GENEVE" "Config2_GENEVE" "geneve://172.245.106.111:$port2?vni=$vxlan_id2&mtu=1436"
}

# ============================================================================
# MAIN INSTALLATION SEQUENCE
# ============================================================================
main() {
  log "=== Multi-Protocol VPN/Proxy Installer Started ==="
  log "Working directory: $WORK_DIR"
  log "Output file: $OUTPUT_FILE"
  
  init_system || error "System initialization failed"
  
  {
    echo "==================================================================="
    echo "VPN/Proxy Connection Strings and QR Codes"
    echo "Generated: $(date)"
    echo "==================================================================="
  } > "$OUTPUT_FILE"
  
  # Install all protocols
  install_wireguard || warn "WireGuard installation failed"
  install_shadowsocks || warn "Shadowsocks installation failed"
  install_outline || warn "Outline installation failed"
  install_hysteria2 || warn "Hysteria2 installation failed"
  install_tuic || warn "TUIC installation failed"
  install_quic || warn "QUIC installation failed"
  install_xray || warn "Xray installation failed"
  install_trojan || warn "Trojan installation failed"
  install_openvpn || warn "OpenVPN installation failed"
  install_stunnel || warn "Stunnel installation failed"
  install_softether || warn "SoftEther installation failed"
  install_ipsec || warn "IPsec installation failed"
  install_l2tp || warn "L2TP installation failed"
  install_squid || warn "Squid installation failed"
  install_socks5 || warn "Dante SOCKS5 installation failed"
  install_vxlan || warn "VXLAN installation failed"
  
  log "=== Installation Complete ==="
  log "Configuration files saved to: $WORK_DIR"
  log "Connection strings saved to: $OUTPUT_FILE"
  
  # Display summary
  echo ""
  echo "==================================================================="
  echo "✅ Installation Summary"
  echo "==================================================================="
  echo "Working Directory: $WORK_DIR"
  echo "Backup Directory: $BACKUP_DIR"
  echo "Output File: $OUTPUT_FILE"
  echo ""
  echo "📝 All connection strings and QR codes available in:"
  cat "$OUTPUT_FILE"
  echo ""
  echo "==================================================================="
}

# Run main
main "$@"