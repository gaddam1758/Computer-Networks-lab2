import os

frame_size=100000
file_name='file.txt'

with open(file_name,'r',encoding="utf8") as f:
    while 1:
        x=f.read(100000)
        if x:
            print(x)
        else:
            break
