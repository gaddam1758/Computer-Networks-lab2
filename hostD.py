import socket
import csv
from _thread import *
import threading

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
usernames = []
attendance = []
filename = "attendance.csv"
with open(filename, "r") as csvfile:

    csvreader = csv.reader(csvfile)

    fields = next(csvreader)
    for row in csvreader:
        per = 0.0
        for i, col in enumerate(row):
            if i == 1:
                usernames.append(col)
            elif i > 1 and col == "Done":
                per = per + 1
        per = per / 8
        attendance.append(per * 100)


# thread function
def threaded(c):

    while True:
        username = c.recv(1024).decode()
        print(username)

        print(username in usernames)
        if username in usernames:
            print("username verified")
            c.send((str(attendance[usernames.index(username)])).encode())
        else :
            c.send(str(-1).encode())  
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

