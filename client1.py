import socket
import os
frame_size = 100000  # 100KB
file_name = 'file.txt'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = input("enter server  ip")
port = int(input("enter server port"))
s.connect((host_ip, port))
print("connected")
# reciel
print(s.recv(1024).decode())
username = input("enter username")
if(username == "EXIT"):
    s.close()
else:
    s.send(username.encode())
    print(s.recv(1024).decode())
    password = input("enter password")
if(password == "EXIT"):
    s.close()
else:
    s.send(password.encode())
    print(s.recv(1024).decode())
    auth = int(s.recv(1024).decode())
    print(auth)
    if(auth):
        with open(file_name, 'r', encoding="utf8") as f:
            while 1:
                x = f.read(frame_size)
                if x:
                    s.send(x.encode())
                else:
                    break
# close the connection
    s.close()
print("Socket closed")
