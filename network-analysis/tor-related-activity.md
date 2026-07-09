# Tor-Related Activity Analysis

## Objective

Determine whether the suspect's machine established genuine connections to the Tor anonymity network, as opposed to merely attempting DNS resolution of `.onion` addresses (see `suspicious-connections.md`).

## Commands Used

### Standard Tor Ports

```bash
tshark -r Daniel_Network.pcap -Y "tcp.port==9001 || tcp.port==9030 || tcp.port==9050 || tcp.port==9150"
```

**Result:** No matching packets found.

### TLS SNI Inspection

```bash
tshark -r Daniel_Network.pcap -Y tls.handshake.extensions_server_name -T fields -e tls.handshake.extensions_server_name
```

**Result:** All observed SNI values corresponded to legitimate services — Microsoft, Bing, MSN, Outlook, OneDrive, Edge, Mozilla, Google APIs, python.org. No TLS handshake to `torproject.org`, `bridges.torproject.org`, or known Tor relay infrastructure was observed.

## Interpretation

Three scenarios were considered to explain the presence of `.onion` DNS queries without corresponding Tor network traffic:

1. **Scenario A (most likely):** The user manually typed a `.onion` address into a standard, non-Tor browser (e.g., Microsoft Edge). The browser issued a DNS query for the address, which failed with no A record (NXDOMAIN-equivalent behavior), and no further connection attempt was made because standard browsers cannot resolve `.onion` addresses without Tor routing.

2. **Scenario B:** A background application or previously bookmarked entry attempted to resolve a `.onion` address automatically, unrelated to active user browsing.

3. **Scenario C:** Tor Browser was used during a period *not covered* by this specific capture window, meaning genuine Tor traffic may exist but simply falls outside the captured timeframe.

## Conclusion

**No definitive evidence of an established Tor connection was found within this capture.** However, the repeated and sequential nature of the `.onion` DNS queries (5 distinct domains, each queried multiple times over a ~15 minute window) strongly indicates **deliberate attempts to access dark web hidden services**, regardless of whether those attempts succeeded via Tor. This finding should be read alongside the disk image examination (browser history, Tor Browser installation artifacts) for a complete picture, as network capture alone cannot confirm or rule out Tor usage outside the capture window.

## Recommendation for Correlation

The disk-analysis team should check for:
- Tor Browser installation artifacts or executables
- Browser history entries for the identified `.onion` domains
- SOCKS proxy configuration settings on the host
