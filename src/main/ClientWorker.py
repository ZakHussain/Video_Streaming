# Author(s): Design and starter code from Kurose, Lab 6, with updates and additions by 
# Cat Smith, Jack Robertson, Zak Hussain

"""

Purpose: 

ClientWorker holds GUI logic and all client-related methods. 

Once ClientLauncher creates ClientWorker and initiates the main() loop, ClientWorker operates in a 
self-contained fashion. It initiates contact with the server via a RTSP request, listens for 
server RTSP messages, initiates the RTP connection, and so forth. ClientWorker calls its own methods 
as necessary in response to server input (in the form of RTSP messages and RTP packets) and user input 
(in the form of mouse clicks).

ClientWorker's responsibility include the following:
    - Broadly, handles all changes to client state.
    - Sends RTSP requests to the server and handles RTSP requests from the server.
    - Creates GUI interface.
    - Sends requests to server in response to user input (via GUI buttons).
    - Changes client state upon receiving server's OK.
    - Opens sockets (for RTP, RTSP) as appropriate.
    - Listens for RTP packets and depacketizes.

- Cat Smith, 7 August 2020

"""

from tkinter import *
import tkinter.messagebox as tkMessageBox
from PIL import Image, ImageTk
import socket, threading, sys, traceback, os
import pickle
from socket import *
from RtpPacket import RtpPacket
import RtspRequest as rq

CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

"""

Design of ClientWorker class is based on finite state machine diagram. States are INIT, READY, or PLAYING. 
Transitions between states are triggered by events (button clicks) which mirror their associated RTSP requests,
namely SETUP, PLAY, PAUSE, and TEARDOWN.

"""
class ClientWorker:
    INIT = 0
    READY = 1
    PLAYING = 2
    state = INIT

    SETUP = 0
    PLAY = 1
    PAUSE = 2
    TEARDOWN = 3

    # Initiation..
    def __init__(self, master, serveraddr, serverport, rtpport, filename):
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.handler)
        self.createWidgets()
        self.serverAddr = serveraddr
        self.serverPort = int(serverport)
        self.rtpPort = int(rtpport)
        self.fileName = filename
        self.rtspSeq = 0
        self.sessionId = 0
        self.requestSent = -1
        self.teardownAcked = 0
        self.connectToServer()
        self.frameNbr = 0

    """
    Build GUI with buttons that mirror associated RTSP requests: SETUP, PLAY, PAUSE, and TEARDOWN.
    """
    def createWidgets(self):
        # Create Setup button
        self.setup = Button(self.master, width=20, padx=3, pady=3)
        self.setup["text"] = "Setup"
        self.setup["command"] = self.setupMovie
        self.setup.grid(row=1, column=0, padx=2, pady=2)

        # Create Play button
        self.start = Button(self.master, width=20, padx=3, pady=3)
        self.start["text"] = "Play"
        self.start["command"] = self.playMovie
        self.start.grid(row=1, column=1, padx=2, pady=2)

        # Create Pause button
        self.pause = Button(self.master, width=20, padx=3, pady=3)
        self.pause["text"] = "Pause"
        self.pause["command"] = self.pauseMovie
        self.pause.grid(row=1, column=2, padx=2, pady=2)

        # Create Teardown button
        self.teardown = Button(self.master, width=20, padx=3, pady=3)
        self.teardown["text"] = "Teardown"
        self.teardown["command"] = self.exitClient
        self.teardown.grid(row=1, column=3, padx=2, pady=2)

        # Create a label to display the movie
        self.label = Label(self.master, height=19)
        self.label.grid(row=0, column=0, columnspan=4, sticky=W + E + N + S, padx=5, pady=5)

    """
    All the button handlers below.
    """
    def setupMovie(self):
        """Setup button handler."""
        if self.state == self.INIT:
            self.sendRtspRequest(self.SETUP)

    def exitClient(self):
        """Teardown button handler."""
        self.sendRtspRequest(self.TEARDOWN)
        self.master.destroy()  # Close the gui window
        self.rtspSocket.close()        
        os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT)  # Delete the cache image from video

    def pauseMovie(self):
        """Pause button handler."""
        if self.state == self.PLAYING:
            self.sendRtspRequest(self.PAUSE)

    def playMovie(self):
        """Play button handler."""
        if self.state == self.READY:
            # Create a new thread to listen for RTP packets
            threading.Thread(target=self.listenRtp).start()
            self.playEvent = threading.Event()
            self.playEvent.clear()
            self.sendRtspRequest(self.PLAY)

    """
    Listen for RTP packets arriving from the server. Call decoding method on packets, parse sequence
    number, and update movie cache with new frame unless arriving packet is out of order.

    @raise exception if PAUSE or TEARDOWN requested, or if socket error
    """
    def listenRtp(self):
        while True:
            try:
                data = self.rtpSocket.recv(20480)
                if data:

                    rtpPacket = RtpPacket()
                    rtpPacket.decode(data)

                    currFrameNbr = rtpPacket.get_seq_num()
                    print("Current Seq Num: " + str(currFrameNbr))

                    if currFrameNbr > self.frameNbr:  # Discard the late packet
                        self.frameNbr = currFrameNbr
                        self.updateMovie(self.writeFrame(rtpPacket.get_payload()))
            except:
                # Stop listening upon requesting PAUSE or TEARDOWN
                if self.playEvent.isSet():
                    break

                # Upon receiving ACK for TEARDOWN request,
                # close the RTP socket
                if self.teardownAcked == 1:
                    self.rtpSocket.shutdown(socket.SHUT_RDWR)
                    self.rtpSocket.close()
                    break

    """
    Write raw RTP payload to cached image file for immediate display by the GUI.

    @param data: raw RTP payload (bytes) which is then written to JPEG file
    """
    def writeFrame(self, data):
        """Write the received frame to a temp image file. Return the image file."""
        cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
        
        try: 
            file = open(cachename, "wb")
            file.write(data)
            file.close()
        except Exception as e: 
            print("Cache not found", str(e))
        return cachename

    """
    Update the image file as video frame in the GUI.
    """
    def updateMovie(self, imageFile):
        photo = ImageTk.PhotoImage(Image.open(imageFile))
        self.label.configure(image=photo, height=288)
        self.label.image = photo

    """
    Use TCP to create RTSP connection to server. Connection attempted upon SETUP and closes with TEARDOWN.
    Subsequent clients will establish a new connection.

    @raise exception if server connection fails to initiate (usually a result of error in input to socket)
    """
    def connectToServer(self):
        """Connect to the Server. Start a new RTSP/TCP session."""
        self.rtspSocket = socket(AF_INET, SOCK_STREAM)
        try:
            self.rtspSocket.connect((self.serverAddr, self.serverPort))
            print("Connected to server... RTSP connection successful.")
        except:
            print("Connection to server address failed.")
            tkMessageBox.showwarning('Connection Failed', 'Connection to \'%s\' failed.' % self.serverAddr)

    """
    Send RTSP requests to server to coordinate change in client state. GUI buttons directly initiate 
    RTSP requests. Any changes in client state must be vetted against current state (for instance, this 
    method will not request PAUSE unless current state is PLAYING). Once a request is vetted, pickle and
    send data via RTSP socket.

    @param requestCode represents integer associated with request type 
    """
    def sendRtspRequest(self, requestCode):
        """Send RTSP request to the server."""

        # Setup request
        if requestCode == self.SETUP and self.state == self.INIT:
            threading.Thread(target=self.recvRtspReply).start()

            # Update RTSP sequence number.
            self.rtspSeq += 1

            # Write the RTSP request to be sent.
            request = rq.RtspRequest("SETUP", self.rtspSeq, self.fileName, self.rtpPort)
            print("Setup request has been sent from sendRtspRequest()")
            # Keep track of the sent request.
            self.requestSent = self.SETUP

        # Play request
        elif requestCode == self.PLAY and self.state == self.READY:
            # Update RTSP sequence number.
            self.rtspSeq += 1

            # Write the RTSP request to be sent.
            request = rq.RtspRequest("PLAY", self.rtspSeq, self.fileName, self.rtpPort)

            # Keep track of the sent request.
            self.requestSent = self.PLAY

        # Pause request
        elif requestCode == self.PAUSE and self.state == self.PLAYING:
            # Update RTSP sequence number.
            self.rtspSeq += 1

            # Write the RTSP request to be sent.
            request = rq.RtspRequest("PAUSE", self.rtspSeq, self.fileName, self.rtpPort)

            # Keep track of the sent request.
            self.requestSent = self.PAUSE

        # Teardown request
        elif requestCode == self.TEARDOWN and not self.state == self.INIT:
            # Update RTSP sequence number.
            self.rtspSeq += 1

            # Write the RTSP request to be sent.
            request = rq.RtspRequest("TEARDOWN", self.rtspSeq, self.fileName, self.rtpPort)

            # Keep track of the sent request.
            self.requestSent = self.TEARDOWN
        else:
            return

        # Send the RTSP request using rtspSocket.
        outgoing = pickle.dumps(request)
        self.rtspSocket.send(outgoing)

        print('\nData sent.')

    """
    Receive RTSP reply from the server. Close RTSP socket if TEARDOWN is requested.
    """
    def recvRtspReply(self):
        while True:
            reply = self.rtspSocket.recv(1024)

            if reply:
                self.parseRtspReply(reply.decode("utf-8"))

            # Close the RTSP socket upon requesting Teardown
            if self.requestSent == self.TEARDOWN:
                self.rtspSocket.shutdown(SHUT_RDWR)
                self.rtspSocket.close()
                break


    """
    Parse the RTSP reply from the server.
    
    @param data is the raw server reply
    """
    def parseRtspReply(self, data):
        lines = data.split('\n')
        seqNum = int(lines[1].split(' ')[1])

        # Process only if the server reply's sequence number is the same as the request's
        if seqNum == self.rtspSeq:
            session = int(lines[2].split(' ')[1])
            # New RTSP session ID
            if self.sessionId == 0:
                self.sessionId = session
            # Process only if the session ID is the same
            if self.sessionId == session:
                if int(lines[0].split(' ')[1]) == 200:
                    if self.requestSent == self.SETUP:
                        # Update RTSP state.
                        self.state = self.READY
                        # Open RTP port.
                        self.openRtpPort()
                    elif self.requestSent == self.PLAY:
                        self.state = self.PLAYING
                    elif self.requestSent == self.PAUSE:
                        self.state = self.READY
                        # The play thread exits. A new thread is created on resume.
                        self.playEvent.set()
                    elif self.requestSent == self.TEARDOWN:
                        self.state = self.INIT
                        # Flag the teardownAcked to close the socket.
                        self.teardownAcked = 1

    
    
    """
    Open RTP socket binded to a specified port.

    @raise error if socket unable to bind
    """
    def openRtpPort(self):
        # Create datagram socket.
        self.rtpSocket = socket(AF_INET, SOCK_DGRAM)

        # Set timeout value (set to .5 seconds)
        self.rtpSocket.settimeout(0.5)

        try:
        # Bind the socket to the address using the RTP port given by the client user
            self.rtpSocket.bind((self.serverAddr, self.rtpPort))
            print('port is bound via the openRtpPort()')
        except:
            print("Unable to bind to port")
            tkMessageBox.showwarning('Unable to Bind', 'Unable to bind PORT=%d' % self.rtpPort)


    """
    Pause movie and check if user wants to quit if user presses GUI window exit button. 
    """
    def handler(self):
       
        self.pauseMovie()
        if tkMessageBox.askokcancel("Quit?", "Are you sure you want to quit?"):
            self.exitClient()
        else:  # When the user presses cancel, resume playing.
            self.playMovie()
