# PyDownloader
Downloads files and folders at high speed (based on your interent speed).

This is very useful to transfer big files from one computer to another.

The client can download any file or folder that is located in servers folder.

![Image of the client](https://raw.githubusercontent.com/ArmenG888/PyDownloader/main/Screenshot/PyDownloaderV0.6.PNG)

<h1> Installation </h1>
1. Download it
<pre> git clone https://github.com/ArmenG888/PyDownloader </pre>
<pre> cd PyDownloader/PyDownloader/ </pre>

2. Install the libraries
Windows 
<pre> pip install -r requirements.txt </pre>
Linux or Mac
<pre> pip3 install -r requirements.txt </pre>
2. Move the client.py
Move the client.py or download to the computer that you want to send files to and put the server.py in the computer from where you want to send.

![Image of the server](https://raw.githubusercontent.com/ArmenG888/PyDownloader/main/Screenshot/server_screenshot.PNG)

<h1> Usage </h1>

When you start you need to type in your ip or port by default it will auto detect ip and 52000 port then you start the server by clicking the button and when the client connects it will pop up a message showing the name of the computer that connected they you need to choose a directory you want for client to be able to download. Then the client chooses the file or folder he wants to download.

![Image of the server choosing file](https://raw.githubusercontent.com/ArmenG888/PyDownloader/main/Screenshot/Capture.PNG)

If you're just testing and download files on the same computer note that the download speed will be very high compared to when connected to different computer and you need to place the client or the server file into another directory or there can be errors.
