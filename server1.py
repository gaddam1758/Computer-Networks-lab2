import socket
import csv
from _thread import *
import threading
import pickle
import hashlib
frame_size = 100256

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
                if(attendance >= 80):

                    c.send(
                        ("You have been granted priveleged connection. Your attendance is "+str(attendance)+"%").encode())
                    c.send("1".encode())
                else:
                    c.send(
                        ("Your credentials have been verified. Your attendance is "+str(attendance)+"%").encode())
                    c.send("1".encode())
            
            ##recieving file
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host,host_port)) 
            print("connected to Host"+row[0])
            s.send("0".encode())
            print(s.recv(1024).decode())
            s.send(username.encode())
            print(s.recv(1024).decode())
            s.send(password.encode())
            filesize = c.recv(1024).decode()
            s.send(filesize.encode())
            frames = c.recv(1024).decode() 
            s.send(frames.encode())     
            while 1:
                packet = c.recv(frame_size)
                if not packet:
                    data = s.recv(1024)
                    if not data:
                        s.close()
                        print("file sent")
                        break
                    else:
                        break
                else:
                    p = pickle.loads(packet)
                    md5 = hashlib.md5()
                    md5.update(packet)
                    if(p[-1]==md5.digest()):
                        s.send(packet)
                        ack=s.recv(1024)
                        c.send(ack)
                    else:
                        c.send("0".encode()) ##checksum failed
                    
                

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
