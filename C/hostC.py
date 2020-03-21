import socket 
import csv
from _thread import *
import threading
import pickle
import hashlib
import sys
import random
from collections import defaultdict
frame_size = 111256


port = int(input("enter port number "))
#creating tcp socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#binding socket to given port
s.bind(('0.0.0.0',port))
print("server binded to port ",port)
HOST=socket.gethostname()
print(HOST)
# become a server socket
s.listen(5)

print("server is listening")

#extracting usernames and passwords from csv file 
usernames = []
passwords = []
filename = "login3.csv"
with open(filename,'r') as csvfile:

       csvreader = csv.reader(csvfile)

       fields = next(csvreader)
       for row in csvreader:
              usernames.append(row[0])
              passwords.append(row[1])
n_frames = {}
user_frames = defaultdict(dict)
#thread functio
def threaded(c):

       while True:
              auth = int(c.recv(1).decode())
              username = (c.recv(1024)).decode()
              print(username)
              c.send("Username received ".encode())
                     
              #Recieve and verify password
              password = (c.recv(1024)).decode()
              print(password)
              if password in passwords and username in usernames and usernames.index(username)==passwords.index(password):

                     c.send("1".encode())
              else:

                     c.send("0".encode())
                     break
              print(auth)
              if not auth:
                     #filename=username+".txt"
                     # filesize = c.recv(1024)
                     # filesize = int.from_bytes(filesize, sys.byteorder)
                     # #print(filesize)
                     frames = c.recv(frame_size)
                     frames = pickle.loads(frames)
                     n_frames[username]=frames
                     # print(filesize)
                     print(frames)
                     while 1:
                            packet = c.recv(frame_size)
                            #print(packet)
                            if not packet:
                                   break
                            else:
                                   p = pickle.loads(packet)
                                   k=p[-1]
                                   del p[-1]
                                   checksum =hashlib.md5(pickle.dumps(p)).digest()
                                   if(k== checksum):
                                          #print(p[0])
                                          #print(p[1])
                                          user_frames[username][p[0]]=p[1]
                                          print("packet"+str(p[0])+" recieved successfully")
                                          c.send("1".encode())
                                          if(p[0]==n_frames[username]):
                                                 f=open(username+".txt","w")
                                                 for key, frame in sorted(user_frames[username].items()):
                                                        f.write(frame)
                                                        print("frame "+str(key)+" written successfully")
                                                 user_frames[username].clear()
                                                 f.close()
                                                 
                                   else:
                                          c.send("0".encode())
                                          print("packet corrupted")
                                          
              #to close socket if client closed the socket
              data = c.recv(frame_size)
              if not data: break


       c.close() 
       print("socket closed")
while True: 

       # Establish connection with client. 
       c, addr = s.accept()      
       
       print('Got connection from', addr) 
       start_new_thread(threaded, (c,))
       # send a thank you message to the client.  
       c.send('Thank you for connecting'.encode()) 
       # Recieve and verify user name
       