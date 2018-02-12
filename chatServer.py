import socket
import time

host = ''
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

quitting = False
print("Server Started.")

while not quitting:
    try:
        data, addr = s.recvfrom(1024)
        if "Quit" in str(data):
            quitting = True
            if addr not in clients:
                clients.append(addr)

                print(time.ctime(time.time()) + str(addr) + ": :" + str(data))
                for client in clients:
                    s.sendto(data, client)
    except:
        pass    # FIXME: Ms Geanne! Why is this code here??
                # Everyone on StackOverflow says that this is terrible programming practice!

s.close()

