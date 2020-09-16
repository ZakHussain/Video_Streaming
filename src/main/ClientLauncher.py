import sys
import socket

# Author(s): Zak Hussain, Cat Smith
# Credit: Kurose lab 6 code 
"""
Purpose: 
 
The ClientLauncher class is used to launch a client application process. 
It does the following: 
1. Reads in user input: 
    * address of server 
    * rtsp port number
    * rtp port number
    * name of filepath for media content to stream
2. It creates a Tkinter obj to pass to the client app, which allows the client 
   to send control packets to the streaming server. 
"""
from tkinter import Tk
from ClientWorker import ClientWorker
class ClientLauncher: 

    def main(self):

        print("Client application is launching")
        # In an actual application, these inputs would be read in from the 
        # command line. 
        serverAddr = '127.0.0.1'
        serverPort = 8000
        rtpPort = '1025'
        fileName = "./movie.Mjpeg"  
        
        # Set the root tKinter object to controll GUI Handles 
        root = Tk()
        
        # Create a new client
        app = ClientWorker(root, serverAddr, serverPort, rtpPort, fileName)

        app.master.title("RTPClient")   
        root.mainloop()

if __name__== "__main__": 
    (ClientLauncher()).main()