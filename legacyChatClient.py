import socket
import threading
import time

import pickle

tlock = threading.Lock()
shutdown = False




def receving(name, sock):
    while not shutdown:
        try:
            tlock.acquire()
            while True:

                data, addr = sock.recvfrom(1024)

                if "gm" in data and "New User Entered!" not in data:
                    if messageType == "gm":
                        print(str(data[2:]))

                elif "New User Entered!" not in data:
                    print(str(data))




        except:
            pass
        finally:
            tlock.release()

def addToGroupChat(clientIndex):

    gcFileWrite = open("gc.csv", "a+")
    member = str(clientIndex) + "\n"
    gcFileWrite.write(member)
    gcFileWrite.close()

def addToPrivateChat(clientIndex):

    pcFileWrite = open("pc.csv", "a+")
    member = str(clientIndex) + "\n"
    pcFileWrite.write(member)
    pcFileWrite.close()

def addToPrivateChat2(clientIndex):

    pcFileWrite = open("pc2.csv", "a+")
    member = str(clientIndex) + "\n"
    pcFileWrite.write(member)
    pcFileWrite.close()

def addToPrivateChat3(clientIndex):

    pcFileWrite = open("pc3.csv", "a+")
    member = str(clientIndex) + "\n"
    pcFileWrite.write(member)
    pcFileWrite.close()


def getClientNumber():
    with open('info.csv') as fp:
        lines = fp.readlines()
        clientNumber = len(lines)
        return clientNumber



host = '127.0.0.1'
port = 0

f = open("info.csv", "r")

clientNumber = -1
server = ('127.0.0.1', 5002)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = raw_input("Name: ")
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

#message = raw_input(alias + "-> ")
message = "New User Entered!"
messageType = raw_input("pm or gm or gc or pc?: ")



if messageType == "pm":
    whatClient = raw_input("What client number?: ")
    #print (alias + ": " + message)

elif messageType == "gc":
    clientNumber = getClientNumber()
    addToGroupChat(getClientNumber())

elif messageType == "pc":
    password = raw_input("Password: ")
    if password == "pc1":
        print "Entered Private Chatroom"
        clientNumber = getClientNumber()
        addToPrivateChat(getClientNumber())
    else:
        print "Incorrect Password"
        messageType = "gm"

elif messageType == "pc2":
    password = raw_input("Password: ")
    if password == "pc2":
        print "Entered Private Chatroom"
        clientNumber = getClientNumber()
        addToPrivateChat2(getClientNumber())
    else:
        print "Incorrect Password"
        messageType = "gm"

elif messageType == "pc3":
    password = raw_input("Password: ")
    if password == "pc3":
        print "Entered Private Chatroom"
        clientNumber = getClientNumber()
        addToPrivateChat3(getClientNumber())
    else:
        print "Incorrect Password"
        messageType = "gm"

while message != 'q':
    if message != '':
        if message == "New User Entered!":
            s.sendto(messageType + alias +", " + message, server)
        else:
            if messageType == "pm":
                s.sendto(whatClient + messageType + alias + ": " + message, server)
            elif messageType == "gc":
                if "inv" in message:
                    index = raw_input("Who would you like to invite?:  ")
                    addToGroupChat(index)
                else:
                    s.sendto(messageType + alias + ": " + message, server)
            elif "pc" in messageType:
                s.sendto(messageType + alias + ": " + message, server)
            else:
                s.sendto(messageType + alias + ": " + message, server)

    # tlock.acquire()
    message = raw_input()
    # time.sleep(0.2)
    # tlock.release()




shutdown = True
rT.join()
s.close()
