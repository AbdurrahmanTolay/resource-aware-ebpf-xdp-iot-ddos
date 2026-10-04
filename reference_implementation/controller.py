"""Reference user-space controller for new replication runs.

This implementation follows the article's verified control-path semantics:
XDP observes IPv4/UDP traffic and returns XDP_PASS; user space estimates
per-source packet rate from cumulative counters; Netfilter/iptables performs
source blocking.

It is a reference reconstruction for reproducibility, not a claim that this
exact source revision generated every historical result in the manuscript.
"""

import argparse
import socket
import struct
import subprocess
import time
from pathlib import Path

from bcc import BPF

COOLDOWN_SECONDS = 30.0

XDP_FLAGS = {
    "skb": 1 << 1,
    "drv": 1 << 2,
    "hw": 1 << 3,
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", required=True, help="Interface to attach the reference XDP monitor")
    parser.add_argument(
        "--xdp-mode",
        choices=sorted(XDP_FLAGS),
        default="skb",
        help="Replication attachment mode; record this choice in the run manifest",
    )
    parser.add_argument("--threshold", type=float, required=True, help="Reference threshold in packets/s")
    parser.add_argument(
        "--source",
        default=str(Path(__file__).with_name("xdp_monitor.c")),
        help="Path to reference XDP source",
    )
    parser.add_argument("--chain", default="IOT_DDOS_TEST", help="Dedicated iptables chain")
    parser.add_argument("--poll-ms", type=float, default=100.0, help="Controller polling interval")
    parser.add_argument(
        "--observe-only",
        action="store_true",
        help="Run the same observation/rate logic without installing DROP rules",
    )
    return parser.parse_args()


def ipv4_from_key(key):
    return socket.inet_ntoa(struct.pack("I", key.value))


def run_quiet(command):
    return subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )


def ensure_firewall_path(chain):
    run_quiet(["sudo", "iptables", "-N", chain])
    if run_quiet(["sudo", "iptables", "-C", "INPUT", "-j", chain]).returncode != 0:
        subprocess.run(["sudo", "iptables", "-I", "INPUT", "1", "-j", chain], check=True)


def ensure_drop_rule(chain, ip_address):
    check = ["sudo", "iptables", "-C", chain, "-s", ip_address, "-j", "DROP"]
    add = ["sudo", "iptables", "-A", chain, "-s", ip_address, "-j", "DROP"]

    if run_quiet(check).returncode != 0:
        subprocess.run(add, check=True)


def monitor_loop():
    args = parse_args()
    flags = XDP_FLAGS[args.xdp_mode]

    if not args.observe_only:
        ensure_firewall_path(args.chain)

    bpf = BPF(src_file=args.source)
    fn = bpf.load_func("xdp_prog_mitigate", BPF.XDP)
    bpf.attach_xdp(args.interface, fn, flags)
    stats = bpf.get_table("src_ip_stats")

    previous_counts = {}
    last_action = {}
    last_check_ns = time.perf_counter_ns()

    mode = "observe-only" if args.observe_only else "enforcing"
    print(
        f"Reference controller active; interface={args.interface} "
        f"xdp_mode={args.xdp_mode} threshold={args.threshold}pps mode={mode}",
        flush=True,
    )

    try:
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

                if args.observe_only:
                    action = "would_block"
                else:
                    ensure_drop_rule(args.chain, ip_address)
                    action = "drop_rule_requested"

                return_ns = time.perf_counter_ns()
                last_action[ip_address] = now_mono

                print(
                    f"source={ip_address} rate_pps={rate_pps:.2f} "
                    f"action={action} controller_action_ms={(return_ns-request_ns)/1e6:.3f}",
                    flush=True,
                )

            last_check_ns = now_ns
    finally:
        BPF.remove_xdp(args.interface, flags)
        print("Reference XDP monitor detached.", flush=True)


if __name__ == "__main__":
    monitor_loop()
