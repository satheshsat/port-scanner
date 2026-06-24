import socket
from concurrent.futures import ThreadPoolExecutor

def check_port(ip: str, port: int, timeout: float = 1.0) -> int | None:
    """
    Attempts to connect to a specific port on the target IP address.
    Returns the port number if it is open, otherwise returns None.
    """
    # AF_INET specifies IPv4, SOCK_STREAM specifies TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        # connect_ex returns 0 if the connection was successful
        result = sock.connect_ex((ip, port))
        if result == 0:
            return port
    return None

def scan_ports(ip: str, start_port: int, end_port: int, max_workers: int = 100):
    """
    Scans a range of ports on a target IP address using multi-threading.
    """
    print(f"\n[+] Starting scan on host: {ip}")
    print(f"[+] Scanning ports from {start_port} to {end_port}...")
    
    open_ports = []
    ports_to_scan = range(start_port, end_port + 1)

    # Use ThreadPoolExecutor to speed up the process through concurrency
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all port scanning tasks to the thread pool
        futures = {executor.submit(check_port, ip, port): port for port in ports_to_scan}
        
        for future in futures:
            port = futures[future]
            try:
                result = future.result()
                if result:
                    print(f"  --> Port {result} is OPEN")
                    open_ports.append(result)
            except Exception as e:
                print(f"Error scanning port {port}: {e}")

    print("\n[+] Scan Complete.")
    if open_ports:
        print(f"[+] Found open ports: {open_ports}")
    else:
        print("[-] No open ports found within the specified range.")

if __name__ == "__main__":
    # Example Inputs
    target_ip = input("Enter the public IP address to scan: ").strip()
    from_port = int(input("Enter the START port (e.g., 20): "))
    to_port = int(input("Enter the END port (e.g., 1024): "))
    
    # Validate port ranges
    if 1 <= from_port <= 65535 and 1 <= to_port <= 65535 and from_port <= to_port:
        scan_ports(target_ip, from_port, to_port)
    else:
        print("[-] Invalid port range configuration.")
