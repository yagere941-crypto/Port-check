# 🔍 Python Port Scanner

A simple, fast, and multi-threaded **TCP port scanner** built using Python.  
This tool scans a target IP address to detect **open ports and common services**.  
It is intended for **educational purposes and authorized security testing only**.

---

## 🚀 Features
- Scan **default common ports** or a **custom port range**
- Multi-threaded scanning using `ThreadPoolExecutor`
- Basic **service identification**
- **Banner grabbing** for common services (FTP, SSH, HTTP, etc.)
- Lightweight and easy to understand
- No external dependencies (uses Python standard library only)

---

## 🛠 Requirements
- Python 3.x

---

## ▶️ Installation

Clone the repository and move into the project directory:

```bash
git clone https://github.com/yagere941-crypto/python-checkport.git
cd python-checkport
```

# ▶️ Usage

Run the script:
```bash
python checkport.py

```

When prompted, enter the target IP address:
```bash
Enter Target IP Address: 127.0.0.1

```
Scan a specific target directly
```bash
python checkport.py 127.0.0.1
```
Scan a custom port range
```bash
python checkport.py 127.0.0.1 1-5000
```

# 📄 Sample Output
- [OPEN] Port 22 (SSH)
- [OPEN] Port 80 (HTTP)
- [OPEN] Port 443 (HTTPS)
