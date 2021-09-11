import socket,os,shutil,sys
from zipfile import ZipFile
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *
from ui_pydownloader import Ui_MainWindow
from hurry.filesize import size
class server(QMainWindow):
    def __init__(self):
        ip = socket.gethostbyname(socket.gethostname())
        port = 52000
        # set up the server and accept the client
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.ip_entry.setText(ip)
        self.ui.port_entry.setText(str(port))
        self.ui.start_server_button.clicked.connect(self.start_server)
        self.show()

    def start_server(self):
        print("start")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ui.ip_entry.text(), int(self.ui.port_entry.text())))
        print(self.ui.ip_entry.text(), self.ui.port_entry.text())
        s.listen(5)
        self.conn, addr = s.accept()
        name = self.conn.recv(1024).decode()
        QMessageBox.information(self, "Connected", name + " has succesfully connected.")
        self.delete_start_screen()
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Folder')
        self.prepare_download(directory)
    def delete_start_screen(self):
        self.ui.ip_entry.deleteLater()
        self.ui.port_entry.deleteLater()
        self.ui.ip_label.deleteLater()
        self.ui.port_label.deleteLater()
        self.ui.start_server_button.deleteLater()

    def prepare_download(self,directory=""):
        print(directory)
        # gets the list of files to send to the client
        if directory != "":
            files = os.listdir(directory)
            os.chdir(directory)
        else:
            files = os.listdir()

        x = ""
        for i in files:
            x += i +","
        self.conn.send(x.encode())
        # receives the name of the file and sends back the size of it
        file = self.conn.recv(1024).decode()

        # checks if is it folder or a file
        a = os.path.isdir(file)
        self.is_dir = "0" if a == True else "1"
        # if its a folder it makes the folder a zip file to send it
        if self.is_dir == "0":
            shutil.make_archive(file, 'zip',file)
            file += ".zip"
        # sends is it a folder or a file to the client
        self.conn.send(self.is_dir.encode())
        # sends the size of the file or folder
        self.file_size = os.path.getsize(file)
        self.conn.send(str(self.file_size).encode())
        # Calls the download function
        self.conn.recv(1024)
        self.download(file)
    def download(self,file):
        # reads the file by 1024 and sends it to the client
        with open(file,"rb") as r:
            while True:
                # reads the data by 1024
                data = r.read(1024)
                if not data:break
                # sends the data
                self.conn.send(data)
        # removes the zip file after the download is over
        if self.is_dir == "0": os.remove(file)
        quit()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = server()
    sys.exit(app.exec_())
