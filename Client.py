import socket #adds socket library
import sys
import time
from _thread import *
import threading 
import os
import subprocess

time.sleep(1)
s = socket.socket()         #Defines Socket
print("Client Initializing...")
host = "127.0.0.1"
name = input(str("Enter your name: "))
port = 9000
s.connect((host,port))
print("\n... Successfully Connected to server\n")
print("Console commands include 'list' and 'message'\n")
print("'list' allows for all active clients to be displayed\n")
print("'message' allows for messaging between clients\n")

def send_name():
    s.send(name.encode())   #sends name to server


def inMessage():
    while 1:
        incoming_message = s.recv(1024)
        incoming_message = incoming_message.decode()
        if (incoming_message == "Identify"):    #Returns the user's name to client(when asked by server)
            s.send(name.encode())
        else:
            print(incoming_message,"\n")

def outMessage():           #Constantly allows for messages to be sent from client
    while 1:
        message = input(str("")) 
        message = message.encode()
        print("\n")
        s.send(message)

t1 = threading.Thread(target=outMessage,) 
t2 = threading.Thread(target=inMessage,)   

send_name()
t1.start() 
t2.start() 
  
t1.join() 
t2.join() 
