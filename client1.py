import socket
import os
import math
import hashlib
import pickle
import sys
from importlib import reload
print(sys.getdefaultencoding())
frame_size = 10000  # 100KB
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
    auth = int(s.recv(1024).decode())
    print(auth)
    if(auth):
        file_size = os.path.getsize(file_name)
        print(file_size)
        # s.send(bytes(file_size))
        # #print(str(file_size).encode()[2])

        # print("k")
        frames = math.ceil(file_size/frame_size)
        s.send(str(frames).encode())
        print(frames)
        with open(file_name, 'rb') as f:
            frame_no = 0
            frame = f.read(frame_size)
            while 1:
                print(sys.getsizeof(frame))
                print(frame)
                if frame:
                    packet = []
                    packet.append(frame_no)
                    packet.append(frame)
                    checksum =hashlib.md5(pickle.dumps(packet)).digest()
                    print(checksum)
                    packet.append(checksum)
                    pkt = pickle.dumps(packet)
                    s.send(pkt)
                    try:
                        s.settimeout(100)
                        ack = s.recv(1024)
                        s.settimeout(None)
                        if(ack):
                           print("acknowledgment recieved")
                           frame = f.read(frame_size)
                           frame_no=frame_no+1
                    except:
                        print("resending frame"+str(frame_no)) 
                        
                else:
                    f.close()
                    break
# close the connection
    s.close()
print("Socket closed")
