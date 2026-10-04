#!/usr/bin/env bash
set -euo pipefail

# Reference replication harness.
# This script does not claim to reconstruct the exact historical execution
# commands of the expanded campaign. Edit environment-specific values and
# archive the resulting commands in the run manifest.

TARGET_IP="${TARGET_IP:?Set TARGET_IP}"
INTERFACE="${INTERFACE:-eth0}"
DURATION="${DURATION:-60}"
RUNS="${RUNS:-10}"
THRESHOLD="${THRESHOLD:-800}"

RATES=(10000 20000 30000 50000 75000)

run_one() {
    local condition="$1"
    local run_id="$2"
    local pps="$3"

    INTERFACE="${INTERFACE}" ./reset_environment.sh

    echo "condition=${condition} run=${run_id} pps=${pps}"

    if [[ "${condition}" == "mitigated" ]]; then
        (
          cd ../reference_implementation
          sudo python3 controller.py --threshold "${THRESHOLD}"
        ) &
        CONTROLLER_PID=$!
        sleep 2
    else
        CONTROLLER_PID=""
    fi

    # Example Mausezahn command. Verify its effective rate on your system and
    # record the exact version/command in the run manifest.
    sudo mz "${INTERFACE}" -A rand -B "${TARGET_IP}" -t udp "dp=80"         -d "$((1000000 / pps))usec" -c "$((pps * DURATION))" &
    ATTACK_PID=$!

    sleep "${DURATION}"

    sudo kill "${ATTACK_PID}" 2>/dev/null || true
    if [[ -n "${CONTROLLER_PID}" ]]; then
        sudo kill "${CONTROLLER_PID}" 2>/dev/null || true
    fi
}

for rate in "${RATES[@]}"; do
    for i in $(seq 1 "${RUNS}"); do
        run_one "unmitigated" "${i}" "${rate}"
    done
    for i in $(seq 1 "${RUNS}"); do
        run_one "mitigated" "${i}" "${rate}"
    done
done
