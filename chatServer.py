# TODO: add if __name__ == "__main__":

import socket
import time

host = '127.0.0.1'
port = 5002

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False
print "Server Started."

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            quitting = True
        if addr not in clients:
            clients.append(addr)
        if "pm" not in data:
            print time.ctime(time.time()) + str(addr) + ": :" + str(data)
            for client in clients:
                s.sendto(data, client)
        else:

            dataSplit = data.split("pm")
            clientIndex = int(dataSplit[0])

            print time.ctime(time.time()) + str(addr) + ": :" + str(data[3:])
            s.sendto(data[3:], clients[clientIndex])
    except:
        pass
s.close()

