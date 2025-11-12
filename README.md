# 🛡️ TwoWaySSLTransfer

A simple, **secure**, and **cross-platform** Python application for two-way file transfer and text processing using **sockets** and **SSL/TLS**.

This project demonstrates a **client-server architecture** where:

- The **Client** sends a text file (`send.txt`) to the **Server**.  
- The **Server** receives the file, counts the frequency of each word, and saves the results.  
- The **Client** can then request the processed file, which the **Server** sends back.  
- All communication is **encrypted**.

---

## How It Works (Protocol Flow)

```
Client                             Server
  |                                  |
  |--- SSL/TLS Handshake ----------> |
  |                                  |
  |--- Send File Size (8 bytes) ---> |
  |--- Send File Data (send.txt) --> |
  |                                  |
  |                                  | <--- Receive & Process File
  |                                  | <--- Save result_for_client.txt
  |                                  |
  |--- Send 'start' command ----->   |
  |                                  |
  | <--- Send File Size (8 bytes) ---|
  | <--- Send File Data (result) ----|
  |                                  |
  |--- Receive & Save result_file.txt|
```

---

##  Features

- **Secure** — All data encrypted with SSL/TLS.  
- **Two-Way Transfer** — Client-to-server and server-to-client communication.  
- **Simple Protocol** — `[8-byte file size] + [file data]` structure.  
- **Cross-Platform** — Tested between macOS (Client) and Windows (Server).  

---

## Requirements

- Python **3.x**  
- Standard libraries: `socket`, `ssl`, `os`, `collections`  
- **OpenSSL** (for generating certificates)

---

## etup & Installation

### 1. Clone the Repository
---

### 2. Generate Security Certificates

Run this command in your project directory:

```bash
openssl req -x509 -newkey rsa:2048 -nodes -keyout server.key -out server.crt -days 365
```

This creates two files:

- `server.key` — your private key  
- `server.crt` — your public certificate  

---

### 3. Prepare the Client File

Ensure your `send.txt` file exists in the project folder and ends with a space and a period (` .`) for accurate word counting.

---

## How to Run

You can run this in two modes:
1. **Localhost (Single Machine)**
2. **Network Mode (Different Machines)**

---

### Localhost Test (Single Machine)

#### Step 1: Edit `client.py`
```python
HOST = 'localhost'
```

#### Step 2: Start the Server
```bash
python3 server.py
```
Expected output:
```
Secure server listening on 0.0.0.0:5000...
```

#### Step 3: Run the Client
```bash
python3 client.py
```

Type `start` and press **Enter** when prompted.

#### Step 4: Check Results
You’ll find a new file:
```
client_result.txt
```
containing the word frequency output.

---

### 🌐 Network Test (Two Machines: macOS Client / Windows Server)

#### On the Server (Windows)

1. **Find IP Address**
   ```bash
   ipconfig
   ```
   Example: `IPv4 Address. . . . . . . . . . . : 172.20.10.9`

2. **Edit `server.py`**
   ```python
   HOST = '0.0.0.0'
   ```

3. **Allow Through Firewall**
   - Open *Windows Defender Firewall with Advanced Security* (`wf.msc`).
   - Create **Inbound Rules**:

**Rule 1 — Python Port 5000:**
- Type: Port → TCP → Port 5000  
- Action: Allow the connection  
- Profile: Domain, Private, Public  
- Name: Python App Port 5000  

**Rule 2 — Allow Ping (for Testing):**
- Type: Custom → Protocol: ICMPv4 → Echo Request  
- Action: Allow connection  
- Profile: Domain, Private, Public  
- Name: Allow All Ping (ICMPv4-In)  

---

#### On the Client (macOS)

1. **Copy Certificate**  
   Copy `server.crt` from the Windows machine to the client project folder.

2. **Edit `client.py`**
   ```python
   HOST = '173.20.10.8'  # Replace with your actual server IP
   ```

3. **Test Connectivity**
   ```bash
   ping 173.20.10.8
   ```
   If you get replies, connection is successful.

4. **Run Client**
   ```bash
   python3 client.py
   ```
   Type `start` and press Enter.

---

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.
