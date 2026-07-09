# Suspicious Connections — Dark Web Domain Queries

## Summary

Analysis of DNS traffic within `Daniel_Network.pcap` revealed multiple repeated queries for `.onion` domains originating from internal host **192.168.40.135**, which is presumed to be the suspect's (Daniel Vega) laptop based on evidence correlation.

## Command Used

```bash
tshark -r Daniel_Network.pcap -Y dns -T fields -e frame.time -e ip.src -e dns.qry.name | grep '\.onion$' | sort -u
```

## Domains Identified

| Domain | First Query Time (WIB) |
|---|---|
| humantradeabcxyz.onion | 10:49:58 |
| shadowdealersxyz.onion | 10:52:07 |
| deepwebroutesxyz.onion | 10:55:25 |
| darkmarketxyz.onion | 10:58:59 |
| redphoenixtrades.onion | 11:02:55 |

All queries originated from `192.168.40.135` and were resolved against the internal DNS server `192.168.40.2`.

## DNS Response Analysis

```bash
tshark -r Daniel_Network.pcap -Y "dns.flags.response==1 && dns.qry.name contains \"onion\"" -T fields -e frame.time -e ip.src -e ip.dst -e dns.a
```

All DNS responses for `.onion` queries returned an **empty `dns.a` field** (no A record). This is consistent with expected behavior, since `.onion` domains are not resolvable through the standard public DNS infrastructure — they require Tor hidden service resolution.

## Significance

The domain name `redphoenixtrades.onion` directly correlates with the darknet alias **"RedPhoenix"** found in `contacts.txt` (network-analysis/extracted-objects/contacts.txt), which was identified as a **Supplier** contact with status "Pending Payment." This correlation strongly links the suspect's network activity to the trafficking contact list recovered separately.

The repeated, sequential nature of the queries (moving from one `.onion` domain to another roughly every 3–4 minutes) suggests deliberate, manual browsing behavior rather than automated or background processes.

## Caveat

DNS query evidence alone demonstrates an *attempt* to resolve `.onion` addresses. It does not by itself prove a successful Tor connection was established — see `tor-related-activity.md` for further analysis of this distinction.
