import socket
import struct

UDP_IP = "127.0.0.1"
UDP_PORT = 5007
    
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
#sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

sock.bind((UDP_IP, UDP_PORT))
#sock2.bind(("127.0.0.1", 5006))

while True:
  data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  #print(data.hex()[0:4])
  #convert to float
  #xyz acceleration and rotation
  print(struct.unpack('f', data[0:4]))
  print(struct.unpack('f', data[4:8]))
  print(struct.unpack('f', data[8:12]))
  print(struct.unpack('f', data[12:16]))
  print(struct.unpack('f', data[16:20]))
  print(struct.unpack('f', data[20:24]))
  #temperature
  print(struct.unpack('f', data[24:28]))
  #Convert to short (2 bytes)
  # hr min sec
  print(struct.unpack('H', data[28:30]))
  print(struct.unpack('H', data[30:32]))
  print(struct.unpack('H', data[32:34]))
  #convert to int (4 bytes)
  #nanoseconds
  print(struct.unpack('i', data[36:40]))
  print(len(data))
  print("next pt")

  # if(data=="hello"):
  #   sock2.sendto("Recieved",("127.0.0.1",5006))
  
  # if(data=='166'):
  #   sock2.send(b'hello')
