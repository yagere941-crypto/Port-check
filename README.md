# 🔍 Python Port Scanner

A simple, fast, and multi-threaded **TCP port scanner** built using Python.  
This tool scans a target IP address to detect open ports and is intended for **educational and authorized security testing only**.

---

## 🚀 Features
- Scans ports from **1 to 5000**
- Multi-threaded scanning using `ThreadPoolExecutor`
- Lightweight and easy to understand
- Adjustable socket timeout
- No external dependencies

---

## 🛠 Requirements
- Python 3.x

---

## ▶️ Installation

Clone the repository:
```bash
git clone https://github.com/yagere941-crypto/python-checkport.git
cd python-checkport

```



# ▶️ Usage

Run the script:
```
python checkport.py

```

When prompted, enter the target IP address:
```
Enter target IP Address: 127.0.0.1

```

# 📄 Sample Output
- [OPEN] Port 22
- [OPEN] Port 80
- [OPEN] Port 443
