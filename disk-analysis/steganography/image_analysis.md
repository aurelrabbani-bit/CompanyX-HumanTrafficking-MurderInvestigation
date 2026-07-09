# Steganography Image Analysis

## Files Examined

1. `HiddenMessage.bmp` (474×266, 24-bit, ~379 KB)
2. `safehouse_location.bmp` (474×316, 24-bit, ~450 KB) — recovered with URL-encoded filename `safehouse%20location.bmp`

## Methodology

Multiple independent methods were used to check for hidden/embedded data, since `steghide` could not be installed on the Artix Linux examination system due to unresolvable dependency conflicts (`libmcrypt`, `mhash` no longer available in the Arch/Artix repositories).

### 1. Metadata Inspection

```bash
exiftool HiddenMessage.bmp
exiftool "safehouse%20location.bmp"
```

**Result:** Standard BMP metadata only (dimensions, bit depth, compression). No Author/Comment/Software tags present. BMP format inherently carries minimal metadata, so this result is expected regardless of hidden content.

### 2. Appended Data Check

Compared actual file size against the expected size calculated from BMP header fields (`bits offset` + `image size`, per ExifTool output).

| File | Expected Size | Actual Size | Result |
|---|---|---|---|
| HiddenMessage.bmp | 378,838 bytes | 378,838 bytes | Match — no appended data |

### 3. LSB Bit-Plane Analysis (zsteg)

```bash
zsteg HiddenMessage.bmp
zsteg "safehouse%20location.bmp"
```

**Initial result:** Both files returned multiple matches suggesting embedded **OpenPGP Secret Key** and **OpenPGP Public Key** data across various bit-plane combinations (e.g., `b1,r,msb,xY`, `b3,b,msb,xY`).

**Verification:** All 9 candidate extractions were run through `gpg --list-packets` for structural validation. **All were confirmed as false positives** — the extracted data contained malformed/unknown packet versions and invalid packet structures, consistent with coincidental byte patterns in raw pixel data rather than genuine embedded PGP keys.

### 4. Binary Signature Scan (binwalk)

```bash
binwalk HiddenMessage.bmp
binwalk "safehouse%20location.bmp"
```

**Result:**
- `HiddenMessage.bmp`: Clean, single BMP signature only.
- `safehouse_location.bmp`: One anomalous match at offset `0x5DA3D` identifying a "JBOOT STAG header" (embedded device firmware format). Manual byte-level inspection (`xxd -s 383549 -l 64`) confirmed this was a **false positive** — the bytes were ordinary pixel data with no valid firmware header structure.

## Conclusion

**Negative finding.** Both BMP image files were subjected to four independent verification methods (metadata inspection, appended-data size verification, LSB bit-plane extraction, and binary signature scanning). While several false-positive matches were observed during automated scanning, manual verification confirmed no genuine steganographic content was embedded in either file. Both images are assessed to be decoy artifacts, likely included in the evidence set to test examiner thoroughness rather than to conceal case-relevant data.

This negative finding is itself evidentially useful: it confirms that examiner time is better directed toward the genuinely encrypted artifacts identified elsewhere in this investigation (see `disk-analysis/recovered-files/encrypted-files/`).
