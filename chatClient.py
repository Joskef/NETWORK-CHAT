import socket
import threading
import time

tlock = threading.Lock()
shutdown = False


def receving(name, sock):
    while not shutdown:
        try:
            tlock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data))
        except:
            pass
        finally:
            tlock.release()


host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 5002)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

alias = raw_input("Name: ")
message = raw_input(alias + "-> ")
while message != 'q':
    if message != '':
        s.sendto(alias + ": " + message, server)
    # tlock.acquire()
    message = raw_input()
    # time.sleep(0.2)
    # tlock.release()

shutdown = True
rT.join()
s.close()

