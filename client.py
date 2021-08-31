import socket,os,time,math,sys
from tkinter import *
from tkinter import ttk
from hurry.filesize import size
import zipfile
ip = '127.0.0.1'
port = 52000
class client:
    def __init__(self,ip,port,root):
        self.root = root
        #connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((ip, port))
        #ui
        self.file_list = Listbox(self.root, height=8, width=50, border=0)
        self.file_list.pack(anchor = "nw")
        self.file_list.bind('<<ListboxSelect>>', self.select_file)
        rec = self.s.recv(1024).decode()
        Button(self.root, text="Download", bd = 0, font = ("calibri", 15), command=self.download).pack()
        self.rec = rec.split(",")
        for i in self.rec:
            self.file_list.insert(END, (i))
    def select_file(self,event):
        #selects the file and gets the index
        self.index = self.file_list.curselection()[0]
        
    def download(self):
        file = self.rec[self.index]
        self.s.send(file.encode())
        file_size = self.s.recv(1024).decode()
        is_dir = self.s.recv(1024).decode()
        is_dir = True if is_dir == "0" else False
        if is_dir == True:
            file_1 = file + ".zip"
        else:
            file_1 = file
        jsonString = bytearray()
        x = 0
        while True:
            packet = self.s.recv(1024)
            x += 1024
            if not packet:
                break
            jsonString.extend(packet)
        with open(file_1, "wb+") as w:
            w.write(jsonString)
        if is_dir == True:
            with zipfile.ZipFile(file_1, 'r') as my_zip:
                my_zip.extractall(file)
            os.remove(file_1)
                
root = Tk()
app = client(ip,port,root)
mainloop()
