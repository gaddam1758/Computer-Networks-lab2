import socket
import os
import math
import hashlib
import pickle

frame_size = 100256  # 100KB
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
        file_size = os.path.getsize(file_name)
        s.send(str(file_size).encode())
        frames = math.ceil(file_size/frame_size)
        s.send(str(frames).encode())
        with open(file_name, 'r', encoding="utf8") as f:
            frame_no = 0
            while 1:
                frame = f.read(frame_size)
                if frame:
                    packet = []
                    packet.append(frame_no)
                    packet.append(frame)
                    md5 = hashlib.md5()
                    md5.update(pickle.dumps(packet))
                    packet.append(md5.digest())
                    pkt = pickle.dumps(packet)
                    s.send(packet)
                    try:
                        s.settimeout(10)
                        ack = s.recv(1024)
                        s.settimeout(None)
                        if(ack):
                           print("acknowledgment recieved")
                           frame = f.read(frame_size)
                    except:
                        print("resending frame"+frame_no) 
                        
                else:
                    break
# close the connection
    s.close()
print("Socket closed")
