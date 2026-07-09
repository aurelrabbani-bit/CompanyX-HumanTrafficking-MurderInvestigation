# Encrypted Files — Decryption Notes

## File 1: hidden.txt

### Initial Observation

`hidden.txt` (41,860 bytes) appeared as plain ASCII text (`file hidden.txt` → "ASCII text") but contained no readable content — entirely composed of high-density printable symbols, inconsistent with natural language or standard encoding schemes.

### Entropy Analysis

```bash
ent hidden.txt
```

Result: **Entropy = 6.337511 bits per byte**, with a statistically significant chi-square deviation (142766.94) indicating the data is *not* random noise, but follows a structured encoding pattern.

### Decoding

Base91 encoding was identified as the likely scheme (alphabet size ~91 chars, theoretical entropy ~6.51 bits/byte, closely matching observed value).

```bash
pip install base91 --break-system-packages
python3 -c "
import base91
data = open('hidden.txt', 'r').read()
decoded = base91.decode(data)
with open('decoded_output.bin', 'wb') as f:
    f.write(bytes(decoded))
"
```

Decoding succeeded structurally (28,951 bytes output). Re-running entropy analysis on the decoded output:

```bash
ent decoded_output.bin
```

Result: **Entropy = 7.987953 bits per byte** — consistent with genuinely encrypted binary data (not a further encoding layer, not plaintext).

### Conclusion

`hidden.txt` is a Base91-encoded, AES-or-equivalent encrypted binary blob. **No key or password was identified** to decrypt the underlying content during this examination phase. This artifact is flagged as **unresolved** and should be revisited if a relevant key is recovered during disk image examination (e.g., private key files, password notes).

---

## File 2: encrypted.zip

### Archive Details

```bash
zipdetails encrypted.zip
```

Key findings:
- **Compression Method:** AES Encryption (WinZip AE-1 format)
- **Encryption Strength:** 256-bit
- Contains 2 files: `contacts.txt` (510 bytes), `safehouse locations.txt` (487 bytes)

### Password Recovery

```bash
zip2john encrypted.zip > hash.txt
john --wordlist=/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt hash.txt
```

**Result:** Password recovered in **7 seconds**:

```
123456           (encrypted.zip/contacts.txt)
123456           (encrypted.zip/safehouse locations.txt)
```

### Extraction and Verification

```bash
7z x encrypted.zip -p123456 -o./extracted_zip/
```

Extraction succeeded. Content comparison confirmed the decrypted files are **identical** to the unencrypted copies of `contacts.txt` and `safehouse_location.txt` already recovered via HTTP object export (see `network-analysis/ftp-http-transfers.md`).

### Conclusion

`encrypted.zip` was successfully decrypted. Despite strong AES-256 encryption, a weak password (`123456`) allowed rapid dictionary-based recovery. The archive's contents were found to be a **redundant backup copy** of the buyer/supplier contact list and safehouse location data already present elsewhere in the evidence set, rather than new information. This nonetheless demonstrates the suspect's inconsistent operational security practices — using strong encryption but a trivially weak password.
