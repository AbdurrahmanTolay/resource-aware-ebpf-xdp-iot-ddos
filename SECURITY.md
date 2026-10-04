# Security and Safe Use

This repository contains privileged networking code and a laboratory traffic-generation harness.

## Intended use

Use it only:

- on hosts you own or administer;
- on an isolated or explicitly authorized test network;
- with targets you have permission to load-test.

The experiment harness requires a private IPv4 target and an explicit `CONFIRM_LAB_ONLY=YES` acknowledgement.

## Privileges

The reference controller and firewall scripts require elevated privileges to:

- attach an XDP program;
- inspect/update BPF state;
- create and modify iptables rules.

Review every command before running it on a production host.

## Firewall behavior

The reference controller creates or reuses the `IOT_DDOS_TEST` chain and inserts a jump from INPUT. Source DROP rules persist until they are flushed or removed. Use `experiments/reset_environment.sh` after a run and verify the resulting firewall state manually.

## Reporting issues

If you find a safety or correctness problem in the replication package, open a GitHub issue without including credentials, private IP information, or sensitive logs.
