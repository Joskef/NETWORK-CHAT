# TODO: add if __name__ == "__main__":

import socket
import time

import pickle


def setGroupChat():
    groupchat = []
    fp = open("gc.csv", "r+")
    lines = fp.readlines()
    for line in lines:
        print "line: " + line
        groupchat.append(clients[int(line)])
    return groupchat

def setPrivateChat():
    privatechat = []
    fpc = open("pc.csv", "r+")
    lines = fpc.readlines()
    for line in lines:
        print "line: " + line
        privatechat.append(clients[int(line)])
    return privatechat

def setPrivateChat2():
    privatechat = []
    fpc = open("pc2.csv", "r+")
    lines = fpc.readlines()
    for line in lines:
        print "line: " + line
        privatechat.append(clients[int(line)])
    return privatechat

def setPrivateChat3():
    privatechat = []
    fpc = open("pc3.csv", "r+")
    lines = fpc.readlines()
    for line in lines:
        print "line: " + line
        privatechat.append(clients[int(line)])
    return privatechat



if __name__ == '__main__':

    host = '127.0.0.1'
    port = 5002

    fileWrite = open("info.csv", "w+")
    fileWrite2 = open("gc.csv", "w+")
    fileWrite3 = open("pc.csv", "w+")
    fileWrite4 = open("pc2.csv", "w+")
    fileWrite5 = open("pc3.csv", "w+")

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
                #if len(clients) % 2 == 1:
                    #groupchat.append(addr)
                clientNames.append((data.split(","))[0])

                fileWrite.write((data.split(","))[0] + "\n")
                fileWrite.close()
                fileWrite = open("info.csv", "a+")

            if "pm" in data:

                dataSplit = data.split("pm")
                clientIndex = int(dataSplit[0])

                print time.ctime(time.time()) + str(addr) + ": :" + str(data[3:])

                s.sendto(data[3:], clients[clientIndex])

            elif "gc" in data:
                print time.ctime(time.time()) + str(addr) + ": :" + str(data[2:])
                groupchat = setGroupChat()
                for gcMember in groupchat:
                    s.sendto(data[2:], gcMember)

            elif "pc2" in data:
                print time.ctime(time.time()) + str(addr) + ": :" + str(data[3:])
                privateChat2 = setPrivateChat2()
                for pcMember in privateChat2:
                    s.sendto(data[3:], pcMember)

            elif "pc3" in data:
                print time.ctime(time.time()) + str(addr) + ": :" + str(data[3:])
                privateChat3 = setPrivateChat3()
                for pcMember in privateChat3:
                    s.sendto(data[3:], pcMember)

            elif "pc" in data:
                print time.ctime(time.time()) + str(addr) + ": :" + str(data[2:])
                privateChat = setPrivateChat()
                for pcMember in privateChat:
                    s.sendto(data[2:], pcMember)

            else:

                print time.ctime(time.time()) + str(addr) + ": :" + str(data[2:])
                clientNames_string = pickle.dumps(clientNames)
                for client in clients:
                    s.sendto(data[2:], client)

        except:
            pass
    s.close()
    fileWrite.close()

