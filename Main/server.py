from tkinter import *
from tkinter import filedialog,messagebox
import socket,os,shutil
from zipfile import ZipFile
# Detects the ipv4 address to use to bind the server
ip = "127.0.0.1"
port = 52000
print("The server is running on IP", ip)
class server:
    def __init__(self,ip,port):
        # set up the server and accept the client
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((ip, port))
        s.listen(5)
        self.conn, addr = s.accept()
        # choose the directory for the client to download
        folder_selected = filedialog.askdirectory()
        self.prepare_download(folder_selected)

    def prepare_download(self,directory=""):

        # gets the list of files to send to the client
        try:
            files = os.listdir(directory)
            os.chdir(directory)
        except Exception:
            files = os.listdir()
        
        x = ""
        for i in files:
            x += i + ","
        self.conn.send(x.encode())
        # receives the name of the file and sends back the size of it
        file = self.conn.recv(1024).decode()

        # checks if is it folder or a file
        a = os.path.isdir(file)
        is_dir = "0" if a == True else "1" 
        # if its a folder it makes the folder a zip file to send it
        if is_dir == "0":
            shutil.make_archive(file, 'zip',file)
            file += ".zip"
        # sends is it a folder or a file to the client
        self.conn.send(is_dir.encode())
        # sends the size of the file or folder
        self.file_size = os.path.getsize(file)
        self.conn.send(str(self.file_size).encode())
        # Calls the download function
        self.download(file)

        if is_dir == "0": os.remove(file)
    def download(self,file):
        # reads the file by 1024 and sends it to the client
        with open(file,"rb") as r:
            while True:
                # reads the data by 1024
                data = r.read(1024)
                if not data:break
                # sends the data
                self.conn.send(data)
app = server(ip,port)
