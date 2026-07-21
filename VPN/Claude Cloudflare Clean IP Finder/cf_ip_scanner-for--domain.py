#!/usr/bin/env python3
"""
cf_ip_scanner.py — find Cloudflare edge IPs that cleanly serve YOUR domain.

Unlike a browser-based scanner, this connects to each candidate IP directly
and sends a TLS ClientHello with SNI = your domain, then an HTTP request with
Host: your-domain — exactly what your VLESS/Xray client does when it connects
through a Cloudflare-fronted config. A browser can't do this: it always ties
SNI/Host to the URL's hostname. Here, they're independent, on purpose.

It verifies Cloudflare's built-in /cdn-cgi/trace endpoint actually reflects
YOUR domain back (the "h=" line), which confirms this edge IP is correctly
routing traffic for your zone — not just "something answered on port 443".

Usage:
    python3 cf_ip_scanner.py --domain claude.amir4v.ir
    python3 cf_ip_scanner.py --domain claude.amir4v.ir --count 30 --workers 50 --timeout 3
    python3 cf_ip_scanner.py --domain claude.amir4v.ir --insecure --verbose

Pure standard library. Requires Python 3.8+.
"""

import argparse
import asyncio
import ipaddress
import random
import re
import ssl
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from typing import List, Optional, Tuple
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# Fallback CIDR list (Cloudflare's official IPv4 ranges as of this writing).
# The script tries to fetch the live list from cloudflare.com first and only
# falls back to this if that fetch fails, so it stays correct over time.
# ---------------------------------------------------------------------------
FALLBACK_RANGES = [
    "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
    "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
    "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
    "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22",
]
CLOUDFLARE_RANGES_URL = "https://www.cloudflare.com/ips-v4"

ANSI_GREEN = "\033[32m"
ANSI_RED = "\033[31m"
ANSI_DIM = "\033[2m"
ANSI_BOLD = "\033[1m"
ANSI_RESET = "\033[0m"


def supports_color() -> bool:
    return sys.stdout.isatty()


def c(text: str, code: str) -> str:
    return f"{code}{text}{ANSI_RESET}" if supports_color() else text


# ---------------------------------------------------------------------------
# Range handling / weighted random IP sampling
# ---------------------------------------------------------------------------

def fetch_live_ranges() -> Optional[List[str]]:
    try:
        with urllib.request.urlopen(CLOUDFLARE_RANGES_URL, timeout=8) as resp:
            text = resp.read().decode("utf-8", errors="replace")
        ranges = [line.strip() for line in text.splitlines() if line.strip()]
        # sanity check: every line should parse as a valid IPv4 network
        for r in ranges:
            ipaddress.ip_network(r, strict=False)
        if ranges:
            return ranges
    except Exception:
        pass
    return None


def prepare_ranges(cidrs: List[str]) -> Tuple[List[Tuple[ipaddress.IPv4Network, int]], int]:
    nets = []
    for cidr in cidrs:
        net = ipaddress.ip_network(cidr, strict=False)
        nets.append((net, net.num_addresses))
    total = sum(size for _, size in nets)
    return nets, total


def random_cloudflare_ip(nets: List[Tuple[ipaddress.IPv4Network, int]], total: int) -> str:
    r = random.uniform(0, total)
    chosen = nets[-1][0]
    for net, size in nets:
        if r < size:
            chosen = net
            break
        r -= size
    net_int = int(chosen.network_address)
    if chosen.num_addresses <= 2:
        offset = random.randint(0, chosen.num_addresses - 1)
    else:
        # avoid network/broadcast addresses
        offset = random.randint(1, chosen.num_addresses - 2)
    return str(ipaddress.ip_address(net_int + offset))


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class TestResult:
    ip: str
    ok: bool
    ms: Optional[float] = None
    status: Optional[int] = None
    colo: Optional[str] = None
    host_seen: Optional[str] = None
    reason: Optional[str] = None


HOST_RE = re.compile(r"^h=(.+)$", re.MULTILINE)
COLO_RE = re.compile(r"^colo=(\S+)$", re.MULTILINE)


async def test_ip(ip: str, domain: str, port: int, path: str, timeout: float,
                   verify: bool, ssl_ctx: ssl.SSLContext) -> TestResult:
    t0 = time.perf_counter()
    writer = None
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port, ssl=ssl_ctx, server_hostname=domain),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        return TestResult(ip=ip, ok=False, reason="timeout")
    except ssl.SSLCertVerificationError as e:
        return TestResult(ip=ip, ok=False, reason=f"tls-cert: {e.reason or e}")
    except ssl.SSLError as e:
        return TestResult(ip=ip, ok=False, reason=f"tls: {e}")
    except (ConnectionRefusedError, OSError) as e:
        return TestResult(ip=ip, ok=False, reason=f"conn: {e}")
    except Exception as e:
        return TestResult(ip=ip, ok=False, reason=f"error: {e}")

    try:
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {domain}\r\n"
            f"User-Agent: cf-ip-scanner/1.0\r\n"
            f"Accept: */*\r\n"
            f"Connection: close\r\n\r\n"
        ).encode()
        writer.write(req)
        await asyncio.wait_for(writer.drain(), timeout=timeout)

        chunks = []
        try:
            while True:
                chunk = await asyncio.wait_for(reader.read(8192), timeout=timeout)
                if not chunk:
                    break
                chunks.append(chunk)
        except asyncio.TimeoutError:
            # Some edges keep the connection open a beat after sending the
            # body; treat whatever we already read as the full response.
            pass

        elapsed_ms = (time.perf_counter() - t0) * 1000
        raw = b"".join(chunks)
        if not raw:
            return TestResult(ip=ip, ok=False, ms=round(elapsed_ms, 1), reason="empty-response")

        head, _, body = raw.partition(b"\r\n\r\n")
        status_line = head.split(b"\r\n", 1)[0].decode(errors="replace")
        parts = status_line.split(" ")
        status_code = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0

        body_text = body.decode(errors="replace")
        host_match = HOST_RE.search(body_text)
        colo_match = COLO_RE.search(body_text)
        host_seen = host_match.group(1).strip() if host_match else None
        colo = colo_match.group(1).strip() if colo_match else None

        ok = status_code == 200 and host_seen is not None and host_seen.lower() == domain.lower()
        reason = None if ok else f"status={status_code} h={host_seen}"

        return TestResult(ip=ip, ok=ok, ms=round(elapsed_ms, 1), status=status_code,
                           colo=colo, host_seen=host_seen, reason=reason)
    except Exception as e:
        return TestResult(ip=ip, ok=False, reason=f"error: {e}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Scanner orchestration
# ---------------------------------------------------------------------------

@dataclass
class Scanner:
    domain: str
    port: int
    path: str
    timeout: float
    worker_count: int
    target_count: int
    max_tested: int
    verify: bool
    verbose: bool
    quiet: bool
    report_every: int

    nets: List[Tuple[ipaddress.IPv4Network, int]] = field(default_factory=list)
    total_weight: int = 0

    tested: int = 0
    clean: List[TestResult] = field(default_factory=list)
    seen_ips: set = field(default_factory=set)
    start_time: float = 0.0
    stop_event: asyncio.Event = field(default_factory=asyncio.Event)

    def make_ssl_context(self) -> ssl.SSLContext:
        ctx = ssl.create_default_context()
        if not self.verify:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        return ctx

    async def worker(self, worker_id: int):
        ssl_ctx = self.make_ssl_context()
        while not self.stop_event.is_set():
            if self.tested >= self.max_tested or len(self.clean) >= self.target_count:
                self.stop_event.set()
                break
            ip = random_cloudflare_ip(self.nets, self.total_weight)
            if ip in self.seen_ips:
                continue
            self.seen_ips.add(ip)

            result = await test_ip(ip, self.domain, self.port, self.path,
                                    self.timeout, self.verify, ssl_ctx)

            if self.stop_event.is_set():
                break

            self.tested += 1
            if result.ok:
                self.clean.append(result)
                if not self.quiet:
                    colo = f" colo={result.colo}" if result.colo else ""
                    print(c(f"  \u2714 {result.ip:<15} {result.ms:>7.1f} ms{colo}", ANSI_GREEN))
            elif self.verbose and not self.quiet:
                print(c(f"  \u2718 {result.ip:<15} {result.reason}", ANSI_DIM))

            if not self.quiet and self.tested % self.report_every == 0:
                elapsed = time.perf_counter() - self.start_time
                print(c(f"  [tested={self.tested} clean={len(self.clean)} "
                        f"elapsed={elapsed:.1f}s]", ANSI_DIM))

    async def run(self):
        self.start_time = time.perf_counter()
        workers = [asyncio.create_task(self.worker(i)) for i in range(self.worker_count)]
        await asyncio.gather(*workers, return_exceptions=True)


def parse_domain(raw: str) -> str:
    raw = raw.strip()
    if "://" in raw:
        parsed = urlparse(raw)
        raw = parsed.hostname or raw
    return raw.rstrip("/")


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Find Cloudflare edge IPs that correctly serve your domain (real SNI + Host, real TLS).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python3 cf_ip_scanner.py --domain claude.amir4v.ir\n"
            "  python3 cf_ip_scanner.py --domain claude.amir4v.ir --count 30 --workers 50 --timeout 3\n"
            "  python3 cf_ip_scanner.py --domain claude.amir4v.ir --verbose --report-every 10\n"
        ),
    )
    p.add_argument("--domain", required=True, help="Your domain (SNI + Host), e.g. claude.amir4v.ir")
    p.add_argument("--port", type=int, default=443, help="Port to test (default: 443)")
    p.add_argument("--path", default="/cdn-cgi/trace", help="Path to request (default: /cdn-cgi/trace)")
    p.add_argument("--count", type=int, default=20, help="Stop after finding this many clean IPs (default: 20)")
    p.add_argument("--max-tested", type=int, default=4000, help="Safety cap on total attempts (default: 4000)")
    p.add_argument("--timeout", type=float, default=4.0, help="Per-attempt timeout in seconds (default: 4.0)")
    p.add_argument("--workers", type=int, default=30, help="Concurrent connections (default: 30)")
    p.add_argument("--insecure", action="store_true", help="Skip TLS certificate verification")
    p.add_argument("--offline", action="store_true", help="Skip fetching the live Cloudflare range list")
    p.add_argument("--verbose", action="store_true", help="Also print failed attempts and why they failed")
    p.add_argument("--quiet", action="store_true", help="Only print the final summary/table")
    p.add_argument("--report-every", type=int, default=25, help="Print a progress line every N attempts (default: 25)")
    p.add_argument("--output", default="cf_clean_ips.txt", help="File to save results to (default: cf_clean_ips.txt)")
    return p


def print_final_table(results: List[TestResult], domain: str, port: int):
    results = sorted(results, key=lambda r: r.ms if r.ms is not None else float("inf"))
    if not results:
        print(c("\nNo clean IPs found. Try --insecure, a longer --timeout, or check that "
                "the domain is actually Cloudflare-proxied (orange cloud) and reachable "
                "from this network.", ANSI_RED))
        return
    print(c(f"\n{len(results)} clean IP(s) for {domain}:443 (verified via matching Host):", ANSI_BOLD))
    print(f"  {'IP':<16}{'ms':>8}   colo")
    for r in results:
        colo = r.colo or "-"
        print(f"  {r.ip:<16}{r.ms:>8.1f}   {colo}")
    print(c("\nPlain list for pasting into a config:", ANSI_DIM))
    print(",".join(r.ip for r in results))


def save_results(results: List[TestResult], path: str, domain: str):
    results = sorted(results, key=lambda r: r.ms if r.ms is not None else float("inf"))
    with open(path, "w") as f:
        f.write(f"# Clean Cloudflare edge IPs for {domain}, sorted by latency\n")
        f.write(f"# ip,ms,colo\n")
        for r in results:
            f.write(f"{r.ip},{r.ms},{r.colo or ''}\n")


async def async_main(args) -> Scanner:
    domain = parse_domain(args.domain)

    ranges = None
    if not args.offline:
        if not args.quiet:
            print(c(f"Fetching live Cloudflare IP ranges...", ANSI_DIM))
        ranges = fetch_live_ranges()
    if ranges is None:
        if not args.quiet:
            note = "offline mode" if args.offline else "fetch failed"
            print(c(f"Using built-in range list ({note}, may drift from Cloudflare's current list).", ANSI_DIM))
        ranges = FALLBACK_RANGES

    nets, total = prepare_ranges(ranges)

    scanner = Scanner(
        domain=domain,
        port=args.port,
        path=args.path,
        timeout=args.timeout,
        worker_count=max(1, args.workers),
        target_count=max(1, args.count),
        max_tested=max(1, args.max_tested),
        verify=not args.insecure,
        verbose=args.verbose,
        quiet=args.quiet,
        report_every=max(1, args.report_every),
    )
    scanner.nets = nets
    scanner.total_weight = total

    if not args.quiet:
        print(c(f"Scanning for {domain} on port {args.port} "
                f"(target: {args.count} clean IPs, {args.workers} workers, "
                f"{'insecure' if args.insecure else 'cert-verified'})...\n", ANSI_BOLD))

    await scanner.run()
    return scanner


def main():
    args = build_arg_parser().parse_args()
    scanner = None
    try:
        scanner = asyncio.run(async_main(args))
    except KeyboardInterrupt:
        print(c("\n\nInterrupted — showing partial results.", ANSI_RED))
    finally:
        if scanner is not None:
            elapsed = time.perf_counter() - scanner.start_time if scanner.start_time else 0.0
            if not args.quiet:
                print(c(f"\nDone. tested={scanner.tested} clean={len(scanner.clean)} "
                        f"elapsed={elapsed:.1f}s", ANSI_DIM))
            print_final_table(scanner.clean, scanner.domain, scanner.port)
            if scanner.clean:
                save_results(scanner.clean, args.output, scanner.domain)
                print(c(f"\nSaved to {args.output}", ANSI_DIM))


if __name__ == "__main__":
    main()
