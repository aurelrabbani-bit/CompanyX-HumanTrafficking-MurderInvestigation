# Cryptocurrency Transaction Leads

## Objective

Identify evidence of cryptocurrency-related transactions or communications within the network capture and associated extracted files, per investigation task III.2.b.

## Network Capture Search

```bash
strings Daniel_Network.pcap | grep -Ei "btc|bitcoin|wallet|xmr|monero|0x[a-f0-9]{40}|bc1[a-z0-9]{25,}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}"
```

**Result:** No direct wallet addresses, transaction IDs, or cryptocurrency keywords were found within the raw packet capture itself.

## Extracted Object Search

While no cryptocurrency artifacts were found directly in network traffic, the HTTP-exported file **client_list.xlsx** (see `ftp-http-transfers.md`) contains an explicit textual reference to cryptocurrency payment requirements:

> "All transactions must be conducted via cryptocurrency (BTC, Monero)."

This note appears in the "Additional Notes" section of the buyer list spreadsheet, alongside four buyer entries with associated payment amounts (ranging from $50,000 to $100,000 USD, with one negotiation marked "???"). See `network-analysis/extracted-objects/client_list.xlsx` and `client_list.csv` for full contents.

## Financial Correlation

A separate document recovered via FTP, **INVOICE.pdf**, shows a $90,000 USD wire transfer between "Quantum Finance Ltd." and "Vega Holdings LLC" (an offshore entity registered in Panama City, Panama), described as "Discreet Asset Management" services. While this transaction uses traditional bank wire rather than cryptocurrency, the entity name "Vega Holdings" directly correlates with suspect Daniel Vega, suggesting a parallel money-laundering channel alongside the cryptocurrency payment method referenced in the buyer list.

## Conclusion

**No recoverable cryptocurrency wallet addresses or blockchain transaction identifiers were found in the captured network traffic.** However, corroborating documentary evidence (client_list.xlsx) confirms that cryptocurrency (BTC, Monero) was the mandated payment method for buyer transactions in this trafficking operation, and a related offshore financial transaction (INVOICE.pdf) provides an additional, non-crypto financial link to the suspect. Both findings should be read together to satisfy the "cryptocurrency and illicit communications" requirement of the investigation task.

## Recommendation for Correlation

The disk-analysis / decryption team should check the suspect's disk image for:
- Cryptocurrency wallet application artifacts (e.g., Electrum, Exodus)
- Browser history for exchange platforms
- Any wallet.dat or key files that may correspond to the buyers listed
