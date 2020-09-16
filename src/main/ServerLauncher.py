import sys
from socket import *

from ServerWorker import ServerWorker

# Author(s): Zak Hussain
# Credit: Kurose lab 6 code 

"""
Purpose: 

Launches the server application for an inputted server port. This 
Class reads in the Server address and desired server port. It 
also prepares a dictionary that stores information pertaining to 
setting up the connections with the client. 
"""
class ServerLauncher: 
    
    def main(self):

        try:
            SERVER_HOSTNAME = 'localhost'
            SERVER_PORT = 8000
        except:
            print("[Usage: Server.py Server_port]\n")
		
        rtspSocket = socket(AF_INET, SOCK_STREAM)
        rtspSocket.bind((SERVER_HOSTNAME, SERVER_PORT))
        rtspSocket.listen(5)        
        print('Server is listening...')
		# Receive client info (address,port) through RTSP/TCP session
        while True:
            # create a dictionary to store client information. 
            clientInfo = {}
            clientInfo['rtspSocket'] = rtspSocket.accept()
            
            # TODO: implement the Server worker class. 
            ServerWorker(clientInfo).run()		

if __name__ == "__main__":
    (ServerLauncher()).main()


