import socket
import sys

host = "0.0.0.0"
port = int(sys.argv[1])
buffer_size = 1024 * 256  # 128KB max size of messages, feel free to increase
# separator string for sending 2 messages in one go
seperator = "<br>"

# Bind the socket to the IP address and listen
s = socket.socket()
s.bind((host, port))
s.listen(5)
print(f"Listening on {host}:{port} ...")

# accept any connections attempted
client_socket, client_address = s.accept()
print(f"{client_address[0]}:{client_address[1]} Connected!")

# receiving the current working directory of the client
cwd = client_socket.recv(buffer_size).decode()
print("Current working directory:", cwd)

while True:
    # get the command from prompt
    command = input(f"{cwd} > ")
    if not command.strip():
        # empty command
        continue
    # send the command to the client
    client_socket.send(command.encode())
    if command.lower() == "exit":
        # if the command is exit, just break out of the loop
        break
    # retrieve command results
    output = client_socket.recv(buffer_size).decode()
    # split command output and current directory
    results, cwd = output.split(seperator)
    # print output
    print(results)

s.close()
