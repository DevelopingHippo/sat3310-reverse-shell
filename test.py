import socket
import os
import subprocess
import sys
from winregistry import WinRegistry

username = os.getlogin()
path = "C:\\Users\\" + username + "\\Documents\\client.py"

print(path)
