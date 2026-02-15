import socket
import time

target = "dmice.ac.in"
print(f"Starting scan on {target}")

start_time = time.time()

for port in range(20, 85):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.setdefaulttimeout(0.5)
	result = s.connect_ex((target, port))
	
	if result == 0:
		print(f"Found Open Port: {port}")
		
	s.close()
	
print(f"Scan done: {time.time() - start_time:.2f}s")