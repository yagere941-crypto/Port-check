# python3 and above version req make sure about it. Thank You
"""
Educational Python Port Scanner (mini-Nmap)
Safe, legal, and educational for network learning.
"""

import argparse
import ipaddress
import json
import logging
import os
import re
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("scan.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class PortScanner:
    def __init__(self, timeout: float = 1.0, threads: int = 100):
        self.timeout = timeout
        self.threads = threads
        self.results = []
        self.scan_stats = {
            "total": 0,
            "open": 0,
            "closed": 0,
            "filtered": 0,
            "errors": 0
        }

    def resolve_hostname(self, target: str) -> str:
        """Convert hostname to IP address."""
        logger.debug(f"Resolving hostname: {target}")
        try:
            ipaddress.ip_address(target)
            return target
        except ValueError:
            try:
                return socket.gethostbyname(target)
            except socket.gaierror:
                raise ValueError(f"Could not resolve hostname: {target}")

    def get_ports(self, ports_arg: Optional[str], top_ports: bool) -> List[int]:
        """Get ports from CLI args or default safe range."""
        if top_ports:
            return [21, 22, 23, 25, 53, 80, 110, 143, 443, 465, 993, 995, 3306, 3389]
        elif ports_arg:
            try:
                start, end = map(int, ports_arg.split('-'))
                return list(range(start, end + 1))
            except (ValueError, IndexError):
                raise ValueError(f"Invalid port range: {ports_arg}. Use format 'start-end'")
        else:
            # Default safe range for educational purposes
            return list(range(1, 1025))

    def scan_port(self, target: str, port: int, stealth: bool = False) -> Optional[Tuple[int, str, str]]:
        """Scan a single port and return results."""
        self.scan_stats["total"] += 1  # Track total ports scanned
        logger.debug(f"Scanning port {port} on {target}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                if stealth:
                    sock.connect((target, port))
                elif sock.connect_ex((target, port)) != 0:
                    self.scan_stats["closed"] += 1
                    return None
                    
                service = self.detect_service(port)
                banner = self.grab_banner(sock, port)
                if banner:
                    service += f" [{banner}]"
                    
                self.scan_stats["open"] += 1
                return (port, "OPEN", service)
        except socket.timeout:
            self.scan_stats["filtered"] += 1
            return (port, "FILTERED", "Timed out")
        except ConnectionRefusedError:
            self.scan_stats["closed"] += 1
            return None
        except Exception as e:
            self.scan_stats["errors"] += 1
            return (port, "ERROR", str(e))

    def detect_service(self, port: int) -> str:
        """Detect service based on port number."""
        service_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
            110: "POP3", 143: "IMAP", 443: "HTTPS", 465: "SMTPS", 993: "IMAPS",
            995: "POP3S", 3306: "MySQL", 3389: "RDP", 1433: "MSSQL", 3306: "MySQL",
            5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
        }
        return service_map.get(port, "Unknown")

    def grab_banner(self, sock: socket.socket, port: int) -> Optional[str]:
        """Grab service banner safely."""
        banner_map = {
            21: b"VERSION\r\n", 22: b"", 23: b"", 25: b"VERSION\r\n", 
            80: b"HEAD / HTTP/1.0\r\nHost: example.com\r\n\r\n",
            443: b"HEAD / HTTP/1.0\r\nHost: example.com\r\n\r\n"
        }
        
        if port not in banner_map:
            return None
            
        try:
            if banner_map[port]:  # Non-empty banner probe
                sock.send(banner_map[port])
            sock.settimeout(self.timeout)
            data = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return data[:50] + "..." if len(data) > 50 else data
        except:
            return None

    def slow_scan(self, target: str, ports: List[int], delay: float = 0.1) -> List[Tuple[int, str, str]]:
        """Scan with rate limiting."""
        logger.info(f"Starting slow scan with {delay}s delay between ports")
        results = []
        for port in ports:
            result = self.scan_port(target, port)
            if result:
                results.append(result)
            time.sleep(delay)
        return results

    def save_results(self, target: str, results: List[Tuple[int, str, str]], 
                    filename: str, fmt: str = 'txt'):
        """Save scan results to file."""
        if fmt == 'json':
            data = {
                "target": target,
                "scan_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "ports": [{"port": r[0], "status": r[1], "service": r[2]} for r in results],
                "stats": self.scan_stats
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
        else:  # TXT
            with open(filename, 'w') as f:
                f.write(f"Port Scan Results for {target}\n")
                f.write("=" * 50 + "\n")
                for port, status, service in results:
                    f.write(f"{status} Port {port}: {service}\n")
                f.write("\nScan Summary:\n")
                for k, v in self.scan_stats.items():
                    f.write(f"{k.capitalize()}: {v}\n")

    def print_results(self, target: str, results: List[Tuple[int, str, str]]):
        """Print formatted scan results."""
        print(f"\nScan Results for {target}")
        print("=" * 50)
        
        for port, status, service in results:
            color = {
                "OPEN": "\033[92m",  # Green
                "FILTERED": "\033[93m",  # Yellow
                "ERROR": "\033[91m"  # Red
            }.get(status, "")
            
            reset = "\033[0m"
            print(f"{color}{status} Port {port}: {service}{reset}")
            
        print("\nScan Summary:")
        print("-" * 30)
        for k, v in self.scan_stats.items():
            print(f"{k.capitalize()}: {v}")

def create_parser():
    """Create argument parser with educational explanations."""
    parser = argparse.ArgumentParser(
        description="Educational Python Port Scanner (mini-Nmap)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Networking Concepts Explained:
- TCP Connect: Standard three-way handshake
- Stealth Scan: TCP connect without SYN flag
- Rate Limiting: Avoids triggering IDS/IPS
- Banner Grabbing: Extracts service info safely
- Thread Pool: Parallel processing for efficiency
        """
    )
    
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("-p", "--ports", help="Port range (e.g., 1-1000)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0, 
                       help="Connection timeout in seconds")
    parser.add_argument("-T", "--threads", type=int, default=100,
                       help="Number of threads for parallel scanning")
    parser.add_argument("--stealth", action="store_true", 
                       help="Use stealth TCP connect scan")
    parser.add_argument("--slow", action="store_true", 
                       help="Enable rate limiting (slower scan)")
    parser.add_argument("--top-ports", action="store_true", 
                       help="Scan common top ports only")
    parser.add_argument("-o", "--output", help="Output file (TXT or JSON)")
    parser.add_argument("--no-color", action="store_true", 
                       help="Disable colored output")
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    print("""
╔═════════════════════════════════════════════╗
║    Educational Port Scanner (mini-Nmap)     ║
║         For learning networking             ║
╚═════════════════════════════════════════════╝
    """)
    
    scanner = PortScanner(timeout=args.timeout, threads=args.threads)
    
    try:
        target = scanner.resolve_hostname(args.target)
        
        # Get ports using new helper function
        ports = scanner.get_ports(args.ports, args.top_ports)
        
        print(f"Scanning {len(ports)} ports on {target}")
        start_time = time.time()
        
        if args.slow:
            results = scanner.slow_scan(target, ports)
        else:
            with ThreadPoolExecutor(max_workers=scanner.threads) as executor:
                futures = {executor.submit(scanner.scan_port, target, p, args.stealth): p 
                          for p in ports}
                
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        scanner.results.append(result)
        
        elapsed = time.time() - start_time
        scanner.print_results(target, scanner.results)
        
        print(f"\nScan completed in {elapsed:.2f} seconds")
        
        if args.output:
            scanner.save_results(target, scanner.results, args.output, 
                               args.output.split('.')[-1].lower())
            print(f"Results saved to {args.output}")
            
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
