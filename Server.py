import socket
import sys
import time
from _thread import *
import threading 
from queue import Queue
import os
import subprocess

Clients = []
Names = []

print("Server Initializing...")

time.sleep(1)
def create_socket():    #creates socket
    try:
        global host
        global port
        global s
        host = "127.0.0.1"
        port = 9000
        s = socket.socket()

    except socket.error as msg:
        print("Socket creation error: " + str(msg))

def bind_socket():      #binds socket
    try:
        global host
        global port
        global s

        s.bind((host, port))
        s.listen(100)

    except socket.error as msg:
        print("Socket binding error" + str(msg) + "\n" + "Retrying...")
        bind_socket()

create_socket()
bind_socket()

def send_message(conn, incoming_message, x, name):      #sends the message with the name of the sender
    message = incoming_message
    conn2 = Clients[x]
    conn2.send(message.encode('utf-8'))  #sends message

    message2 = ("From: ")   
    conn2.send(message2.encode('utf-8'))        #Adds the sender's name to the message
    message3 = (name)
    conn2.send(message3.encode('utf-8'))

    console(conn)   #returns user to console function

def get_message(conn, x):       #takes message from the user
    response = ("Enter in the message")
    conn.send(response.encode('utf-8'))
    
    incoming_message = conn.recv(1024) 
    incoming_message = incoming_message.decode()
    
    identify = ("Identify")     #Asks the client for the user's name
    conn.send(identify.encode('utf-8'))
    
    name = conn.recv(1024)      #Recieves the user's name
    name = name.decode()
    
    send_message(conn, incoming_message, x, name)
    
def message(conn):         #expands on the message command by asking the user who they wish to message
    response = ("Which user would you like to communicate with?")
    conn.send(response.encode('utf-8'))
    incoming_message = conn.recv(1024) 
    incoming_message = incoming_message.decode()

    for i in range(100):
        if incoming_message == Names[i]:
            x = i
            get_message(conn, x)
    
    response = ("Invalid Response")
    conn.send(response.encode('utf-8'))
    console(conn)   #returns user to console function

def console(conn):      #Allows clients to enter in one of two commands, list and message
    while True:
        incoming_message = conn.recv(1024) 
        incoming_message = incoming_message.decode()
        
        if incoming_message == "list":
            print("\nListing connections ...\n",Names)
            response = ', '.join(Names)
            conn.send(response.encode('utf-8'))
            
        if incoming_message == "message":
            message(conn)

def clientthread(conn):   #Takes the name of the newly entered client
    while True:
        s_name = conn.recv(1024)
        s_name = s_name.decode ()
        
        if not s_name:
            break;
        
        Names.append(s_name) 
        print(s_name," has joined")
        console(conn)
        
        #alert = ("... Successfully Connected to SERN")
        #conn.send(alert.encode('utf-8'))
        #print(Names[x],"'s connection point is ", Clients[x])
        
    conn.close

def accepting_connections():    #Accepts new connections and creates new threads
    while True:
        conn, addr = s.accept()
        print("Connected with " + addr[0] + ":" +str(addr[1]))
        
        Clients.append(conn)
        start_new_thread(clientthread, (conn,))

accepting_connections()
