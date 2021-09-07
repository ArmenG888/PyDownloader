import socket,os,time,math,sys,datetime
from tkinter import *
from tkinter.ttk import Progressbar
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
        self.file_list = Listbox(self.root, height=8, width=80, border=0)
        self.file_list.pack(anchor = "nw")
        self.file_list.bind('<<ListboxSelect>>', self.select_file)
        Button(self.root, text="Download", bd =0, font = ("calibri", 15), command=self.download_ask).pack(side=LEFT,anchor='w')
        self.progress = Progressbar(self.root, orient = HORIZONTAL,
              length = 100, mode = 'determinate')
        self.progress.pack(side=LEFT,anchor='w')
        self.percent_label = Label(self.root, text="0%", font=('calibri',15))
        self.percent_label.pack(side=LEFT,anchor='w')
        self.info_label = Label(self.root, text="", font=('calibri',12))
        self.info_label.pack(side=LEFT,anchor='w')
        self.available_files = available_files.split(",")
        # Inserts all of the available files to the list box
        for i in self.available_files:
            self.file_list.insert(END, (i))
    def select_file(self,event):
        # selects the file and gets the index
        self.index = self.file_list.curselection()[0]
        self.file = self.available_files[self.index]
    def download_ask(self):
        x = messagebox.askquestion("Question", "Do you want to download "+self.file+"?")
        if x == "yes":
            self.download()
    def refresh(self):
        self.root.update()
        self.root.after(1000,self.refresh)
    def download(self):
        # sends the file name to download
        self.s.send(self.file.encode())
        # recieves whether its a file or a folder
        is_dir = self.s.recv(1024).decode()
        is_dir = True if is_dir == "0" else False
        # recieves the size of the file
        file_size = self.s.recv(1024).decode()
        file_size_con = size(int(file_size))
        print(file_size_con)

        # changes the file name whether its a zip file(folder) or a normal file
        if is_dir == True:
            file_1 = self.file + ".zip"
        else:
            file_1 = self.file
        jsonString = bytearray()
        mbpersecond_var = 0
        x = 0
        y = 0
        self.s.send("0".encode())
        # downloads by 1024
        start = time.time()
        speed = "0"
        time_left = "NA"
        while True:

            # Updates all of the ui
            percentage = round(x/int(file_size)*100)
            self.percent_label.config(text=str(percentage) + "%")
            self.info_label.config(text="  " + size(x) + "/" + file_size_con +"  "+ speed +" Mib/s   ETA: " + time_left)
            self.progress['value'] = percentage
            # recieves the packet by 1024
            packet = self.s.recv(1024)
            # counts how much data it has recieved
            mbpersecond_var += 1024
            x += 1024
            y += 1
            # refreshes the tkinter for it to not freeze
            if y == 5000:
                y = 0
                self.refresh()
            if size(mbpersecond_var) == "1M":
                mbpersecond_var = 0
                # stops the timer and resets the variable when it's 1M
                end = time.time()
                # gets the speed of the download
                speed = str(round(1/(end-start), 1))
                # starts new timer
                start = time.time()
                # Gets the estimated time of the download
                time_ = round((int(file_size)-x) / 1000000 / float(speed))
                time_left = str(datetime.timedelta(seconds=time_))
            if not packet:
                break
            jsonString.extend(packet)
        # writes the file
        with open(file_1, "wb+") as w:
            w.write(jsonString)
        if is_dir == True:
            # extracts the zip file into a folder if the client was downloading folder
            with zipfile.ZipFile(file_1, 'r') as my_zip:
                my_zip.extractall(self.file)
            # removes the zip file
            os.remove(file_1)
        # success message
        messagebox.showinfo("Success", self.file + " has succesfully downloaded")
        # resets all of the ui
        self.progress['value'] = 0
        self.percent_label.config(text="0%")
        self.root.update_idletasks()
# Creates a tkinter window
root = Tk()
app = client(ip,port,root)
mainloop()
