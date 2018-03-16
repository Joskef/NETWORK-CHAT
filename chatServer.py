# TODO: add if __name__ == "__main__":

import socket
import time

import pickle



if __name__ == '__main__':

    host = '127.0.0.1'
    port = 5002

    fileWrite = open("info.csv", "w+")

    clients = []
    clientNames = []

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.bind((host, port))
    except socket.error as e:
        if e.errno == 98:
            print "Port already in use"
        else:
            print (e)
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
                clientNames.append((data.split(","))[0])

                fileWrite.write((data.split(","))[0] + "\n")
                fileWrite.close()
                fileWrite = open("info.csv", "a+")

            if "pm" not in data:
                print time.ctime(time.time()) + str(addr) + ": :" + str(data)
                clientNames_string = pickle.dumps(clientNames)
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
    fileWrite.close()

