# FTP / HTTP Transfers

## FTP Session Analysis

### Session Log (via TCP stream follow)

```
220 (vsFTPd 3.0.5)
OPTS UTF8 ON
200 Always in UTF8 mode.
USER ftpuser
331 Please specify the password.
PASS anonymous
230 Login successful.
PORT 192,168,40,135,198,18
200 PORT command successful. Consider using PASV.
NLST
150 Here comes the directory listing.
226 Directory send OK.
...
PORT 192,168,40,135,198,23
200 PORT command successful. Consider using PASV.
RETR INVOICE.pdf
150 Opening BINARY mode data connection for INVOICE.pdf (47128 bytes).
226 Transfer complete.
QUIT
221 Goodbye.
```

### Key Findings

- The suspect authenticated to an FTP server (vsFTPd 3.0.5) using account `ftpuser` with password `anonymous` — indicating an unsecured or intentionally open anonymous-style FTP service.
- A directory listing (`NLST`) was performed prior to the file retrieval, suggesting the suspect was actively browsing available files rather than downloading a known target directly.
- The suspect successfully retrieved **INVOICE.pdf** (47,128 bytes) via `RETR`.

## HTTP Object Export

### Command Used

```bash
tshark --export-objects http,http_objects -r Daniel_Network.pcap
```

### Objects Recovered

| File | Notes |
|---|---|
| HiddenMessage.bmp | Analyzed for steganography — see `disk-analysis/steganography/image_analysis.md` |
| safehouse_location.bmp | Analyzed for steganography — see `disk-analysis/steganography/image_analysis.md` |
| Shipment_List.pdf | Contains victim shipment manifest — see Key Findings below |
| client_list.xlsx | Contains buyer list and payment records |
| encrypted.zip | Password-protected archive — see `disk-analysis/recovered-files/encrypted-files/` |

### HTTP Host Analysis

```bash
tshark -r Daniel_Network.pcap -Y http.host -T fields -e http.host
```

The majority of HTTP host entries correspond to legitimate Microsoft/Mozilla/Google background services (telemetry, certificate revocation checks, weather widgets). One notable recurring entry was `192.168.40.135:8080`, suggesting a local web service or proxy running on the suspect's own machine — this warrants further investigation by the disk image examination team, as it may correspond to a local tool used to stage or serve the exfiltrated files above.

## Significance

The combination of FTP and HTTP-retrieved files directly ties the suspect's machine to the core evidentiary documents of the case: the shipment manifest (naming victim "Anna Carter," matching case background victim A.C.), the buyer/client list (explicitly referencing cryptocurrency payment), and the encrypted archive later confirmed to contain duplicate copies of the trafficking contact list.
