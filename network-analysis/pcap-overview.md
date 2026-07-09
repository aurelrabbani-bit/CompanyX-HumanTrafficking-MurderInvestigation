# PCAP Overview — Daniel_Network.pcap

## Evidence Details

| Field | Value |
|---|---|
| File name | Daniel_Network.pcap |
| File size | ~18 MB |
| Source | Captured network traffic from suspect Daniel Vega's laptop |
| Examiner | Fathir Barhouti Awlya (Network Forensic Analyst) |
| Tools used | tshark (Wireshark CLI), strings |
| Environment | Artix Linux |

## Protocol Overview

Initial protocol hierarchy inspection was performed using:

```bash
tshark -r Daniel_Network.pcap -q -z io,phs
```

The capture contains a mix of legitimate background traffic (Microsoft telemetry, Bing, MSN, Windows Update services, Mozilla Firefox services) alongside several suspicious artifacts detailed in the accompanying documents:

- `suspicious-connections.md` — DNS queries to `.onion` domains
- `ftp-http-transfers.md` — FTP session and HTTP object export findings
- `tor-related-activity.md` — Tor port/traffic analysis
- `crypto-transaction-leads.md` — Cryptocurrency-related evidence

## Top Destination IPs

```bash
tshark -r Daniel_Network.pcap -T fields -e ip.dst | sort | uniq -c | sort -nr | head -30
```

The most active destination was the internal host itself (192.168.40.135, 17181 packets), followed by Microsoft/Azure-related infrastructure (40.99.68.34, 52.98.32.2, etc.) and internal DNS server 192.168.40.2. No single external IP stood out as disproportionately dominant, consistent with normal background OS/browser telemetry traffic overlaid with the suspicious activity described in the linked documents.

## Methodology Note

All analysis was performed using command-line tools (`tshark`) rather than the Wireshark GUI, consistent with the Artix Linux terminal-based workflow used throughout this investigation. Each command and its corresponding output was screenshotted and archived in `screenshots/wireshark/` for evidentiary purposes.
