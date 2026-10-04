/*
 * Reference reconstruction for the article replication package.
 *
 * IMPORTANT:
 * This file is consistent with the manuscript's described IPv4/UDP observation
 * and per-source counter state, but it is NOT claimed to be the exact archived
 * source revision used for the expanded historical campaign.
 *
 * Enforcement is deliberately not performed here: packets return XDP_PASS.
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
            val->packets++;
        else
            src_ip_stats.update(&src_ip, &init_val);
    }

    return XDP_PASS;
}
