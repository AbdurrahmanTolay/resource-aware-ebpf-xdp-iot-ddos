"""Reference reconstruction of the manuscript's user-space control role.

This program is provided to make the described mechanism executable for new
replication work. It is NOT claimed to be the exact controller revision used
for every historical result in the article.

It estimates packet rate from cumulative per-source BPF counters over elapsed
controller polling intervals, then requests source blocking via a dedicated
iptables chain. Historical campaign rate-window semantics were not archived.
"""

import argparse
import socket
import struct
import subprocess
import time

from bcc import BPF

COOLDOWN_SECONDS = 30.0


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--threshold", type=float, required=True, help="Reference threshold in packets/s")
    parser.add_argument("--source", default="xdp_monitor.c", help="Path to reference XDP source")
    parser.add_argument("--chain", default="IOT_DDOS_TEST", help="Dedicated iptables chain")
    parser.add_argument("--poll-ms", type=float, default=100.0, help="Controller polling interval")
    return parser.parse_args()


def ipv4_from_key(key):
    return socket.inet_ntoa(struct.pack("<I", key.value))


def ensure_drop_rule(chain, ip_address):
    check = ["sudo", "iptables", "-C", chain, "-s", ip_address, "-j", "DROP"]
    add = ["sudo", "iptables", "-A", chain, "-s", ip_address, "-j", "DROP"]

    if subprocess.run(check, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        subprocess.run(add, check=True)


def monitor_loop():
    args = parse_args()
    bpf = BPF(src_file=args.source)
    stats = bpf.get_table("src_ip_stats")

    previous_counts = {}
    last_action = {}
    last_check_ns = time.perf_counter_ns()

    print(f"Reference controller active; threshold={args.threshold} pps")

    while True:
        time.sleep(args.poll_ms / 1000.0)
        now_ns = time.perf_counter_ns()
        elapsed = (now_ns - last_check_ns) / 1e9
        if elapsed <= 0:
            continue

        for key, value in stats.items():
            ip_address = ipv4_from_key(key)
            current = int(value.packets)
            previous = previous_counts.get(ip_address, current)
            rate_pps = max(0.0, (current - previous) / elapsed)
            previous_counts[ip_address] = current

            if rate_pps <= args.threshold:
                continue

            now_mono = time.monotonic()
            if now_mono - last_action.get(ip_address, float("-inf")) < COOLDOWN_SECONDS:
                continue

            request_ns = time.perf_counter_ns()
            ensure_drop_rule(args.chain, ip_address)
            effective_request_return_ns = time.perf_counter_ns()
            last_action[ip_address] = now_mono

            print(
                f"source={ip_address} rate_pps={rate_pps:.2f} "
                f"iptables_call_ms={(effective_request_return_ns-request_ns)/1e6:.3f}"
            )

        last_check_ns = now_ns


if __name__ == "__main__":
    monitor_loop()
