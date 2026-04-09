# 🔍 Python Port Scanner (checkport.py)

A fast, lightweight, multi-threaded **TCP port scanner** written in Python for detecting **open ports**, performing **basic service identification**, and optional **banner grabbing**.

> ⚠️ For educational use and authorized security testing only.

> Note: Parts of this documentation were refined with the assistance of AI(chatgpt) tools to enhance clarity and readability.

---

## 🚀 Features
- Scan **default ports**, **top ports**, or **custom ranges**
- Multi-threaded scanning (`ThreadPoolExecutor`)
- Basic **service detection** (HTTP, SSH, FTP, etc.)
- **Banner grabbing** for selected services
- Configurable timeout, threads, and scan modes
- No external dependencies (standard library only)

---

## 🛠 Requirements
- Python 3.7+

---

## 📦 Installation
```bash
git clone https://github.com/yagere941-crypto/python-checkport.git
cd python-checkport
```
## ▶️ How to Use
1. Run the script with a target IP address or hostname:
```bash
python checkport.py <target>
```
2. The scanner will:

- Resolve the target (IP/hostname)
- Scan selected ports
- Identify open ports and services
- Display results in the terminal

3. Optionally, customize the scan using flags:

- Define port range
- Enable slow scan
- Scan common ports only
- Save results to a file

## 💻 Usage Examples
```bash 
# Basic scan
python checkport.py 127.0.0.1

# Custom port range
python checkport.py 127.0.0.1 -p 1-5000

# Scan top ports
python checkport.py 127.0.0.1 --top-ports

# Slow scan (rate-limited)
python checkport.py 127.0.0.1 --slow

# Save results
python checkport.py 127.0.0.1 -o results.txt
```
## 📄 Sample Output
```bash 
Scan Results for 127.0.0.1
==================================================
OPEN     Port 22   : SSH
OPEN     Port 80   : HTTP
OPEN     Port 443  : HTTPS

Scan Summary:
------------------------------
Total: 1000
Open: 3
Closed: 997
Filtered: 0
Errors: 0

Scan completed in 2.14 seconds
Scan results have been successfully saved to results.txt.
```

---

## 🧰 Technologies & Modules Used

This project is built entirely using Python’s **standard library**, making it lightweight and dependency-free. Below are the key modules used and their purpose:

### 🔹 `socket`
- Core module for network communication
- Used to create TCP connections to target ports
- Enables port scanning and banner grabbing

### 🔹 `concurrent.futures`
- Provides `ThreadPoolExecutor` for multithreading
- Allows scanning multiple ports simultaneously
- Greatly improves performance compared to sequential scanning

### 🔹 `argparse`
- Handles command-line arguments
- Enables flexible usage with flags like:
  - `-p` (port range)
  - `--top-ports`
  - `--slow`
  - `-o` (output file)

### 🔹 `ipaddress`
- Validates whether input is a proper IP address
- Helps distinguish between IPs and hostnames

### 🔹 `logging`
- Provides structured logging
- Logs scan activity to both console and file (`scan.log`)
- Useful for debugging and tracking scans

### 🔹 `json`
- Used to export scan results in JSON format
- Makes output machine-readable and easy to integrate with other tools

### 🔹 `time`
- Measures scan duration
- Implements delay in slow scan mode (rate limiting)

### 🔹 `os` & `sys`
- Handle system-level operations and program exit handling

---

## 🎯 Why This Approach?

- ✅ **No external dependencies** → Easy to run anywhere  
- ✅ **Fast performance** → Multithreading with controlled concurrency  
- ✅ **Beginner-friendly** → Uses core Python concepts  
- ✅ **Extendable** → Can be upgraded with advanced scanning techniques  

---

