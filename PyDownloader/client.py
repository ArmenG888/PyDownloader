import sys,platform,socket,time,datetime
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from ui_downloader import Ui_Main
from hurry.filesize import size
ip_port = ('192.168.56.1', 52000)
class client(QMainWindow):
    def __init__(self,ip_port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            try:
                self.s.connect(ip_port)
                break
            except Exception:
                continue
        self.s.send(socket.gethostname().encode())
        available_files = self.s.recv(1024).decode()
        QMainWindow.__init__(self)
        self.ui = Ui_Main()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.available_files = available_files.split(",")
        for i in self.available_files:
            self.ui.fielist.addItem(i)
        self.ui.fielist.itemClicked.connect(self.ask_to_download)
        self.ui.exit_button.clicked.connect(self.close)
        self.show()
    def ask_to_download(self,item):
        reply = QMessageBox.question(self, "Downloader", "Do you really want to download " + item.text(), QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.download(item)
    def download(self,item):
        self.file = item.text()
        self.s.send(self.file.encode())
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
        self.s.send("0".encode())
        # downloads by 1024
        start = time.time()
        start_time_elapsed = time.time()
        speed = "0"
        time_left = "NA"

        while True:
            # Updates all of the ui
            percentage = round(x/int(file_size)*100)
            self.ui.progressBar.setValue(percentage)
            self.ui.Info_label.setText("  " + size(x) + "/" + file_size_con +"  "+ speed +" Mib/s   ETA: " + time_left)
            # recieves the packet by 1024
            packet = self.s.recv(1024)
            # counts how much data it has recieved
            mbpersecond_var += 1024
            x += 1024

            if size(mbpersecond_var) == "1M":
                mbpersecond_var = 0
                end = time.time()
                # stops the timer and resets the variable when it's 1M
                # gets the speed of the download
                speed = str(round(1/((end-start)+0.0000000000001), 1))
                # starts new timer
                start = time.time()
                # Gets the estimated time of the download
                time_ = round((int(file_size)-x) / 1000000 / float(speed))
                time_left = str(datetime.timedelta(seconds=time_))

            if not packet:
                break

            jsonString.extend(packet)
        # writes the file
        self.ui.Info_label.setText("Writing the file...")
        with open(file_1, "wb+") as w:
            w.write(jsonString)
        end_time_elapsed = time.time()
        time_elapsed = str(datetime.timedelta(seconds=round(end_time_elapsed-start_time_elapsed)))
        self.ui.Info_label.setText(" Time it took to download:" + time_elapsed)
        if is_dir == True:
            # extracts the zip file into a folder if the client was downloading folder
            with zipfile.ZipFile(file_1, 'r') as my_zip:
                my_zip.extractall(self.file)
            # removes the zip file
            os.remove(file_1)
        QMessageBox.information(self, "Succes", "The file " + self.file +" has succesfully been downloaded.")
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = client(ip_port)
    sys.exit(app.exec_())
