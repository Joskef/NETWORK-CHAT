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
                if "New User Entered!" not in data:
                    print(str(data))

                client_names = f.readlines()
                print "Client Names: \n"
                for clientName in client_names:
                    print(clientName)
        except:
            pass
        finally:
            tlock.release()

host = '127.0.0.1'
port = 0

f = open("info.csv", "r")


server = ('127.0.0.1', 5002)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

alias = raw_input("Name: ")
rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

#message = raw_input(alias + "-> ")
message = "New User Entered!"
pm = raw_input("pm or gm?: ")



if pm == "pm":
    whatClient = raw_input("What client number?: ")
    #print (alias + ": " + message)
while message != 'q':
    if message != '':
        if message == "New User Entered!":
            s.sendto(alias +", " +message, server)
        else:
            if pm == "pm":
                s.sendto(whatClient + pm + alias + ": " + message, server)
            else:
                s.sendto(alias + ": " + message, server)

    # tlock.acquire()
    message = raw_input()
    # time.sleep(0.2)
    # tlock.release()

shutdown = True
rT.join()
s.close()
