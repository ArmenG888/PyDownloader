import socket,os,time,math,sys
from tkinter import *
from tkinter import filedialog,messagebox
from hurry.filesize import size
import zipfile
ip = '127.0.0.1'
port = 52000
class client:
    def __init__(self,ip,port,root):
        self.root = root
        self.root.title("Downloader")
        # connect
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect((ip, port))
                break
            except Exception:
                continue
        # recieves the files that are available to download from server
        available_files = self.s.recv(1024).decode()
        # creates the list box for to show the files that the client can download
        self.file_list = Listbox(self.root, height=8, width=50, border=0)
        self.file_list.pack(anchor = "nw")
        self.file_list.bind('<<ListboxSelect>>', self.select_file)
        
        Button(self.root, text="Download", bd = 0, font = ("calibri", 15), command=self.download).pack()
        self.available_files = available_files.split(",")
        # Inserts all of the available files to the list box
        for i in self.available_files:
            self.file_list.insert(END, (i))
    def select_file(self,event):
        # selects the file and gets the index
        self.index = self.file_list.curselection()[0]
        
    def download(self):
        file = self.available_files[self.index]
        # sends the file name to download
        self.s.send(file.encode())
        # recieves the size of the file and whether its file or a folder
        file_size = self.s.recv(1024).decode()
        is_dir = self.s.recv(1024).decode()
        is_dir = True if is_dir == "0" else False
        # changes the file name whether its a zip file(folder) or a normal file
        if is_dir == True:
            file_1 = file + ".zip"
        else:
            file_1 = file
        jsonString = bytearray()
        x = 0
        # downloads by 1024
        while True:
            packet = self.s.recv(1024)
            x += 1024
            if not packet:
                break
            jsonString.extend(packet)
        # writes the file
        with open(file_1, "wb+") as w:
            w.write(jsonString)
        if is_dir == True:
            # extracts the zip file into a folder if the client was downloading folder
            with zipfile.ZipFile(file_1, 'r') as my_zip:
                my_zip.extractall(file)
            # removes the zip file
            os.remove(file_1)
        # success message
        messagebox.showinfo("Success", file + " has succesfully downloaded")
# Creates a tkinter window
root = Tk()
app = client(ip,port,root)
mainloop()
