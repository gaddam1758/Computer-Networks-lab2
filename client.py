import socket
import os
import math
import hashlib
import pickle
import sys
import random
from importlib import reload
print(sys.getdefaultencoding())
frame_size = 1000  # 100KB
file_name = 'file.txt'
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip_1 = input("enter server  ip for server1")
port_1 = int(input("enter server port for server1"))
host_ip_2 = input("enter server  ip for server2")
port_2 = int(input("enter server port for server2"))
s1.connect((host_ip_1, port_1))
print("connected to server1")
s2.connect((host_ip_2, port_2))
print("connected to server2")
# reciel
print(s1.recv(1024).decode())
print(s2.recv(1024).decode())
username = input("enter username")
if(username == "EXIT"):
    s1.close()
    s2.close()
else:
    s1.send(username.encode())
    print(s1.recv(1024).decode())
    s2.send(username.encode())
    print(s2.recv(1024).decode())
    password = input("enter password")
if(password == "EXIT"):
    s1.close()
    s2.close()
else:
    s1.send(password.encode())
    auth = int(s1.recv(1024).decode())
    s2.send(password.encode())
    auth = auth or int(s2.recv(1024).decode())
    print(auth)
    if(auth):
        p = float(input("enter probability"))
        file_size = os.path.getsize(file_name)
        # print(file_size)
        # s.send(bytes(file_size))
        # #print(str(file_size).encode()[2])

        # print("k")
        frames = math.ceil(file_size/frame_size)
        n=int(p*frames)
        l=[]
        for i in range(0,n):
            l.append(random.randrange(0,frames))
        # s.send(bytes(frames))
        # print(frames)
        print(l)
        with open(file_name, 'rb') as f:
            frame_no = 1
            frame = f.read(frame_size)
            while 1:
                print(sys.getsizeof(frame))
                print(frame_no)
                if frame and (frame_no%2):
                    packet = []
                    packet.append(frame_no)
                    packet.append(frame)
                    checksum =hashlib.md5(pickle.dumps(packet)).digest()
                    print(checksum)
                    packet.append(checksum)
                    pkt = pickle.dumps(packet)
                    if(frame_no in l):
                        l.remove(frame_no)
                        packet[1]="sdsdsdsdsdsdsd"
                        pkt = pickle.dumps(packet)
                    s1.send(pkt)
                    try:
                        s1.settimeout(100)
                        ack = s1.recv(1024)
                        s1.settimeout(None)
                        if(ack):
                           print("acknowledgment recieved from server 1")
                           frame = f.read(frame_size)
                           frame_no=frame_no+1
                    except:
                        print("resending frame"+str(frame_no)) 
                elif frame and not (frame_no%2):
                    
                    packet = []
                    packet.append(frame_no)
                    packet.append(frame)
                    checksum =hashlib.md5(pickle.dumps(packet)).digest()
                    print(checksum)
                    packet.append(checksum)
                    pkt = pickle.dumps(packet)
                    if(frame_no in l):
                        l.remove(frame_no)
                        packet[1]="sdsdsdsdsdsdsd"
                        pkt = pickle.dumps(packet)
                    s2.send(pkt)
                    try:
                        s2.settimeout(100)
                        ack = s2.recv(1024)
                        s2.settimeout(None)
                        if(ack):
                           print("acknowledgment recieved from server 2")
                           frame = f.read(frame_size)
                           frame_no=frame_no+1
                    except:
                        print("resending frame"+str(frame_no)) 
                elif(frame_no>frames):
                    f.close()
                    break
                    
# close the connection
    s1.close()
    s2.close
print("Sockets closed")
