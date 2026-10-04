#!/usr/bin/env bash
set -euo pipefail

# Safe reference harness for NEW laboratory replication runs.
# It is not a reconstruction of every historical command used in the article.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
RESULTS_DIR="${REPO_ROOT}/results"
mkdir -p "${RESULTS_DIR}"

: "${CONFIRM_LAB_ONLY:?Set CONFIRM_LAB_ONLY=YES after confirming you are testing an authorized lab target}"
if [[ "${CONFIRM_LAB_ONLY}" != "YES" ]]; then
    echo "Refusing to run: CONFIRM_LAB_ONLY must be exactly YES." >&2
    exit 1
fi

TARGET_IP="${TARGET_IP:?Set TARGET_IP to an authorized private IPv4 target}"
INTERFACE="${INTERFACE:-eth0}"
DURATION="${DURATION:-20}"
RUNS="${RUNS:-3}"
THRESHOLD="${THRESHOLD:-800}"
POLL_MS="${POLL_MS:-100}"
XDP_MODE="${XDP_MODE:-skb}"
PACKET_SIZE="${PACKET_SIZE:-1200}"

read -r -a RATES <<< "${RATES:-10000 20000 30000 50000 75000}"

python3 - "${TARGET_IP}" <<'PY'
import ipaddress
import sys

ip = ipaddress.ip_address(sys.argv[1])
if ip.version != 4 or not ip.is_private:
    raise SystemExit("TARGET_IP must be a private IPv4 address for this reference harness.")
PY

if ! command -v mz >/dev/null 2>&1; then
    echo "Mausezahn (mz) is required for this harness." >&2
    exit 1
fi

COMMIT_SHA="$(git -C "${REPO_ROOT}" rev-parse HEAD 2>/dev/null || echo unknown)"
MANIFEST="${RESULTS_DIR}/replication_runs.csv"

if [[ ! -f "${MANIFEST}" ]]; then
    echo "timestamp_utc,commit_sha,condition,run_id,target_ip,interface,xdp_mode,threshold_pps,attack_rate_pps,packet_size_bytes,duration_s,controller_log,attack_log" > "${MANIFEST}"
fi

cleanup() {
    if [[ -n "${ATTACK_PID:-}" ]]; then
        sudo kill "${ATTACK_PID}" 2>/dev/null || true
    fi
    if [[ -n "${CONTROLLER_PID:-}" ]]; then
        sudo kill -INT "${CONTROLLER_PID}" 2>/dev/null || true
        wait "${CONTROLLER_PID}" 2>/dev/null || true
    fi
}
trap cleanup EXIT INT TERM

run_one() {
    local condition="$1"
    local run_id="$2"
    local pps="$3"

    ATTACK_PID=""
    CONTROLLER_PID=""

    INTERFACE="${INTERFACE}" bash "${SCRIPT_DIR}/reset_environment.sh"
    sudo bash "${REPO_ROOT}/reference_implementation/firewall_setup.sh"

    local stamp
    stamp="$(date -u +%Y%m%dT%H%M%SZ)"
    local prefix="${RESULTS_DIR}/${stamp}_${condition}_${pps}pps_r${run_id}"
    local controller_log="${prefix}_controller.log"
    local attack_log="${prefix}_attack.log"

    controller_args=(
        "--interface" "${INTERFACE}"
        "--xdp-mode" "${XDP_MODE}"
        "--threshold" "${THRESHOLD}"
        "--poll-ms" "${POLL_MS}"
    )
    if [[ "${condition}" == "unmitigated" ]]; then
        controller_args+=("--observe-only")
    fi

    (
        cd "${REPO_ROOT}/reference_implementation"
        sudo python3 controller.py "${controller_args[@]}"
    ) >"${controller_log}" 2>&1 &
    CONTROLLER_PID=$!
    sleep 2

    local delay_us=$((1000000 / pps))
    local packet_count=$((pps * DURATION))

    echo "condition=${condition} run=${run_id} pps=${pps} packet_size=${PACKET_SIZE}"

    sudo mz "${INTERFACE}"         -A rand         -B "${TARGET_IP}"         -t udp "dp=80,p=${PACKET_SIZE}"         -d "${delay_us}usec"         -c "${packet_count}" >"${attack_log}" 2>&1 &
    ATTACK_PID=$!

    sleep "${DURATION}"

    sudo kill "${ATTACK_PID}" 2>/dev/null || true
    ATTACK_PID=""

    sudo kill -INT "${CONTROLLER_PID}" 2>/dev/null || true
    wait "${CONTROLLER_PID}" 2>/dev/null || true
    CONTROLLER_PID=""

    printf '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
'         "${stamp}" "${COMMIT_SHA}" "${condition}" "${run_id}" "${TARGET_IP}"         "${INTERFACE}" "${XDP_MODE}" "${THRESHOLD}" "${pps}" "${PACKET_SIZE}"         "${DURATION}" "${controller_log}" "${attack_log}" >> "${MANIFEST}"
}

for rate in "${RATES[@]}"; do
    for i in $(seq 1 "${RUNS}"); do
        run_one "unmitigated" "${i}" "${rate}"
    done
    for i in $(seq 1 "${RUNS}"); do
        run_one "mitigated" "${i}" "${rate}"
    done
done

echo "Replication logs written under ${RESULTS_DIR}"
