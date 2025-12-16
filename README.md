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
git clone https://github.com/yourusername/python-port-scanner.git
cd python-port-scanner

```



# ▶️ Usage

Run the script:
```
python port_scanner.py

```

When prompted, enter the target IP address:
```
Enter target IP Address: 192.168.1.1

```

# 📄 Sample Output
- [OPEN] Port 22
- [OPEN] Port 80
- [OPEN] Port 443
