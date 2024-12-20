from socket import *
import sys

# Check arguments
if len(sys.argv) <= 1:
    print('Usage: python ProxyServer.py <server_ip>')
    sys.exit(2)

# Create and set up the proxy server
proxy_socket = socket(AF_INET, SOCK_STREAM)
proxy_socket.bind(('localhost', 8888))  # Use localhost and port 8888
proxy_socket.listen(5)  # Allow up to 5 connections

print("Proxy server ready to serve...")

while True:
    # Accept client connections
    client_socket, addr = proxy_socket.accept()
    print(f"Connection from: {addr}")

    # Receive client request
    message = client_socket.recv(4096).decode()
    if not message:
        client_socket.close()
        continue

    try:
        # Extract filename from request
        filename = message.split()[1].partition("/")[2]
        print(f"Requested file: {filename}")

        # Try reading from cache
        with open(filename, 'rb') as f:
            data = f.read()
            client_socket.sendall(b"HTTP/1.0 200 OK\r\n\r\n" + data)
            print("Served from cache")
    except FileNotFoundError:
        # File not in cache, fetch from the web
        try:
            host = filename.split('/')[0]
            web_socket = socket(AF_INET, SOCK_STREAM)
            web_socket.connect((host, 80))

            web_socket.sendall(f"GET /{filename} HTTP/1.0\r\nHost: {host}\r\n\r\n".encode())
            response = web_socket.recv(4096)

            # Save response to cache and forward to client
            with open(filename, 'wb') as cache_file:
                cache_file.write(response)
            client_socket.sendall(response)
            print("Fetched from web and cached")
        except Exception as e:
            print(f"Error fetching from web: {e}")
            client_socket.sendall(b"HTTP/1.0 404 Not Found\r\n\r\n")
    finally:
        client_socket.close()
