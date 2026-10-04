/*
 * Reference XDP monitor for new replication runs.
 *
 * This file matches the article's verified physical-path role: IPv4/UDP
 * observation and cumulative per-source state, with packets returned via
 * XDP_PASS. It is not claimed to be the exact source revision used for every
 * historical result.
 */

#include <uapi/linux/bpf.h>
#include <linux/in.h>
#include <linux/if_ether.h>
#include <linux/ip.h>

struct stats_value {
    __u64 packets;
};

BPF_HASH(src_ip_stats, __u32, struct stats_value);

int xdp_prog_mitigate(struct xdp_md *ctx)
{
    void *data_end = (void *)(long)ctx->data_end;
    void *data = (void *)(long)ctx->data;

    struct ethhdr *eth = data;
    if ((void *)(eth + 1) > data_end)
        return XDP_PASS;

    if (eth->h_proto != bpf_htons(ETH_P_IP))
        return XDP_PASS;

    struct iphdr *iph = data + sizeof(*eth);
    if ((void *)(iph + 1) > data_end)
        return XDP_PASS;

    if (iph->protocol == IPPROTO_UDP) {
        __u32 src_ip = iph->saddr;
        struct stats_value *val;
        struct stats_value init_val = { .packets = 1 };

        val = src_ip_stats.lookup(&src_ip);
        if (val)
            __sync_fetch_and_add(&val->packets, 1);
        else
            src_ip_stats.update(&src_ip, &init_val);
    }

    /* Observation only. Enforcement remains in Netfilter/iptables. */
    return XDP_PASS;
}
