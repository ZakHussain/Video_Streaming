Original Authors: 
Kurose  
cboehmsmith (Catherine)  
jack-robs  
ZakHussain  

# Changes Underway: 
ZakHussain 9/15/2020
I will be updating this code base to work on an embedded system, and stream content over multiple devices.

# pythonLiveStream
Live Streaming, Python

Contents:
- Technical specs
- Manifest
- What is GH Projects, specifics
- High level flow of work

## Tech Specs
- Media format: mjpeg (jpeg frames)
- Error correction (primary): FEC
- Language: Python 3.x + 

## Manifest 
```
$ tree
.
├── README.md
├── src
│   ├── main
│   │   ├── ClientLauncher.py
│   │   ├── ClientWorker.py
│   │   ├── IRtpPacket.py
│   │   ├── movie.Mjpeg
│   │   ├── RtpPacket.py
│   │   ├── RtspRequest.py
│   │   ├── rtsp_request_test.py
│   │   ├── ServerLauncher.py
│   │   ├── ServerWorker.py
│   │   └── VideoStream.py
│   ├── readme.md
│   └── tests
│       └── rtp_packet_tests.py
└── UMLs
    └── readme.md

4 directories, 14 files
```

## UML
- TODO....

## File explanations

### Client (includes GUI)

**ClientLauncher.py**
- what:
- fields:
  -
- methods:
  -

**ClientWorker.py**
- what: 
- fields:
  -
- methods:
  - 


**ClientWorker.py -> GUI Code**
- what: the code in ClientWorker.py that supports the GUI
- fields (that support the GUI)
  - `self.setup`: button that tells client to send setup request to server, via `self.setupMovie() -> sendRtspRequest(self.SETUP)` logic 
  - `self.start`: button that tells client to send 'play' request to server, via `self.playMovie() -> sendRtspRequest(self.PLAY)` (includes threading)
  - `self.pause`: button that tells client to send 'pause' request to server, via `self.pauseMovie() -> sendRtspRequest(self.PAUSE)`
  - `self.teadown`: button that tells client to send 'teaurdown' request to server, via `self.exitClient() -> sendRtspRequest(self.
- relevant methods 
  - `createWidgets()`: creates buttons via tkinter 
  - note: ClientLauncher.py builds overall GUI window
  - `updateMovie(self, imageFile)`: uses PIL to create an image file that will work w/ the tkinter gui from a jpeg that is stored via cacheName. 



### Server
**ServerLauncher.py**
- what:
- fields:
  -
- methods:
  -

**ServerWorker.py**
- what:
- fields:
  -
- methods: 
  -

### Supporting Class files

**RtspRequest.py**
- what: class for RTSP request objects, has input validation
- fields:
  - reqType: string, the type of request. must match list of allowed request tpes
  - seqNum: integer, the sequence number of the packet the request is in. determined by client/server interactions
  - fileName: the fileName used for the request
  - rtpPort: port used for the RTP connection
- methods:
  - @property and @field.setter for each field (getters/setters)
  - each had input validation and raises exceptions for failures

**RtpPacket.py**
- what: class for RTP packets objects
- fields:
  -
- methods:
  - 


**VideoStream.py**
- what: class for Video frames
- fields:
  - filename: string, filename each frame is written to
- methods:
