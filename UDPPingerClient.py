from socket import *
import time

# Server details
serverName = "127.0.0.1"  # Localhost
serverPort = 12000

# Create a UDP socket
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)  # Set timeout to 1 second

for i in range(1, 11):  # Send 10 pings
    # Create the ping message
    sendTime = time.time()
    message = f"Ping {i} {sendTime}"

    try:
        # Send the message to the server
        clientSocket.sendto(message.encode(), (serverName, serverPort))

        # Wait for the response
        response, serverAddress = clientSocket.recvfrom(1024)
        receiveTime = time.time()

        # Calculate Round Trip Time (RTT)
        rtt = receiveTime - sendTime

        print(f"Reply from {serverAddress}: {response.decode()} RTT = {rtt:.6f} seconds")

    except timeout:
        # Handle timeout (packet loss)
        print(f"Request timed out for Ping {i}")

# Close the socket
clientSocket.close()
