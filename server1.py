import socket
import csv
from _thread import *
import threading
import pickle
import hashlib
import sys
import time
import random
frame_size = 111256

port = int(input("enter port number "))
# creating tcp socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# binding socket to given port
s.bind(("0.0.0.0", port))
print("server binded to port ", port)
HOST = socket.gethostname()
print(HOST)
# become a server socket
s.listen(5)

print("server is listening")

# extracting usernames and passwords from csv file
# usernames = []
# passwords = []
# filename = "login_credentials.csv"
# with open(filename,'r') as csvfile:

#        csvreader = csv.reader(csvfile)

#        fields = next(csvreader)
#        for row in csvreader:
#               usernames.append(row[0])
#               passwords.append(row[1])

# thread function


def threaded(c):

    while True:
        username = (c.recv(1024)).decode()
        if not username:
            c.close()
            print("socket is closed")
            return
        print(username)
        c.send("Username received ".encode())

        # Recieve and verify password
        password = (c.recv(1024)).decode()
        if not password:
            c.close()
            print("socket is closed")
            return
        print(password)
        with open("host_name.rtl", 'r') as csvfile:

            csvreader = csv.reader(csvfile, delimiter='|')
            a = 0 
            for i in range(3):
                row = next(csvreader)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                port = row[2]
                host_ip = row[1]
                print(port, host_ip)
                s.connect((host_ip, int(port)))
                print("connected to Host"+row[0])
                print(s.recv(1024).decode())
                s.send("1".encode())
                s.send(username.encode())
                print(s.recv(1024).decode())
                s.send(password.encode())
                k = int(s.recv(1024).decode())
                a = a or k
                if(k):
                    host = host_ip
                    host_port = int(port)
                # close the connection
                s.close()
                print("Socket closed")
            if a == 0:
                c.send("Invalid Login details".encode())
                c.send("0".encode())
                return
            else:
                row = next(csvreader)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                port = row[2]
                host_ip = row[1]
                print(port, host_ip)
                s.connect((host_ip, int(port)))
                print("connected to Host"+row[0])
                s.send(username.encode())
               #print(s.recv(1024).decode())
                print(s.recv(1024).decode())
                attendance = float(s.recv(1024).decode())
                s.close()
                c.send("1".encode())
            
            ##recieving file
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,host_port)) 
            print(host_port)
            print("connected to Host")
            s.send("0".encode())
            print(s.recv(1024).decode())
            t1=time.time()
            s.send(username.encode())
            print(s.recv(1024).decode())
            t2=time.time()
            rtt=(t2-t1)
            print(rtt)
            s.send(password.encode())
            print(s.recv(1024).decode())
            # filesize = c.recv(1024)
            # print(filesize)
            # print(int.from_bytes(filesize, sys.byteorder))
            # s.send(filesize)
            # print("ssds")
            frames = c.recv(frame_size)
            # print(int.from_bytes(filesize, sys.byteorder))
            s.send(frames)
            print(pickle.loads(frames))     
            while 1:
                try:
                    packet = c.recv(frame_size)
                    if not packet:
                            s.close()
                            print("file sent")
                            break
                    else:
                        p = pickle.loads(packet)
                        k=p[-1]
                        del p[-1]
                        checksum =hashlib.md5(pickle.dumps(p)).digest()
                        print(k)
                        print(checksum)
                        if(k==checksum):
                            #print(p)
                            s.send(packet)
                            
                            print("packet no "+str(p[0])+" sent")
                            ack=s.recv(1024)
                            k=random.randrange(0,5)
                            time.sleep(rtt+k)
                            c.send(ack)
                        else:
                            print("packet corrupted")
                            c.send(str(0).encode()) ##checksum failed
                except:
                    break    
                
        data = c.recv(1024)
        # to close socket if client closed the socket
        if not data:
            break

    c.close()
    print("socket closed")


while True:

    # Establish connection with client.
    c, addr = s.accept()

    print("Got connection from", addr)
    start_new_thread(threaded, (c,))
    # send a thank you message to the client.
    c.send("Thank you for connecting".encode())
    # Recieve and verify user name
