import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_PORTS = [21, 22, 23, 25, 80, 443, 8080, 3306, 3389]

def scan_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                service = get_service_name(port)
                banner = get_banner(s, port)
                if banner:
                    service += f" [{banner}]"
                return (port, f"[OPEN] Port {port} ({service})")
    except Exception as e:
        return (port, f"Error scanning port {port}: {e}")
    return None

def get_service_name(port):
    services = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
        80: "HTTP", 443: "HTTPS", 8080: "HTTP-Alt",
        3306: "MySQL", 3389: "RDP", 53: "DNS", 139: "NetBIOS",
        445: "SMB", 110: "POP3", 143: "IMAP", 389: "LDAP",
        636: "LDAPS", 993: "IMAPS", 995: "POP3S"
    }
    return services.get(port, "Unknown")

def get_banner(sock, port):
    try:
        if port in [21, 22, 23, 25, 80, 8080]:
            if port in [80, 8080]:
                sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            sock.settimeout(1)
            data = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            if data:
                return data[:30] + "..." if len(data) > 30 else data
    except:
        pass
    return None

def parse_port_range(range_str):
    try:
        start, end = map(int, range_str.split('-'))
        if start > end:
            raise ValueError("Start port must be less than end port")
        return range(start, end + 1)
    except ValueError:
        print("Invalid port range. Use format: 1-1000")
        sys.exit(1)

def main():
    try:
        if len(sys.argv) > 1:
            target = sys.argv[1]
        else:
            target = input("Enter target IP Address: ")
        
        if len(sys.argv) > 2:
            ports_to_scan = parse_port_range(sys.argv[2])
        else:
            ports_to_scan = DEFAULT_PORTS
        
        open_ports = []
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = {executor.submit(scan_port, target, p): p for p in ports_to_scan}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    open_ports.append(result)
        
        open_ports.sort(key=lambda x: x[0])
        
        print(f"\nScan completed. Found {len(open_ports)} open ports.")
        if open_ports:
            print("\nOpen ports:")
            for _, port_info in open_ports:
                print(port_info)
    
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
