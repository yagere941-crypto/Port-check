import socket
from concurrent.futures import ThreadPoolExecutor

target = input("Enter target IP Address: ")

def scan_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        if s.connect_ex((target, port)) == 0:
            print(f"[OPEN] Port {port}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, range(1, 5001))
