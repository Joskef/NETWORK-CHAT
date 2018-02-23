from Tkinter import *
import socket
import threading
import time

tlock = threading.Lock()
shutdown = False

'''
def receving(name, sock):
    while not shutdown:
        try:
            tlock.acquire()
            while True:
                data, addr = sock.recvfrom(1024)
                print(str(data) + " hi")
        except:
            pass
        finally:
            tlock.release()




s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=receving, args=("RecvThread", s))
rT.start()

alias = 'null'
'''
host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 5002)
message = 'null'



class LoginWindow:
    def __init__(self, master):
        self.master = master
        frame = Frame(master)
        frame.pack()


        self.titleMessage = Label(frame, text="Enter Username")
        self.textInput = Entry(frame)
        self.textSubmit = Button(frame, text="Login")
        self.textFeedback = Label(frame)

        self.titleMessage.grid(row=0)
        self.textInput.grid(row=1, sticky=W + E)
        self.textSubmit.grid(row=2, sticky=W + E)
        self.textFeedback.grid(row=3, stick=W + E)

        self.textSubmit.bind("<Button-1>", self.loginUser)
        master.bind('<Return>', self.loginUser)

    def loginUser(self, event):
        print("loginUser function accessed")
        if len(self.textInput.get()) == 0:
            self.textFeedback.config(text = "Please Enter a Username!", fg = "red")
        else:
            tempUserString = 'null'
            tempUserString = self.textInput.get()
            self.textFeedback.config(text="Successfully logged in!", fg="dark green")
            self.newWindow = Toplevel(self.master)
            self.client = ChatWindow(self.newWindow, tempUserString) # create new window and pass the new username string to the new window

class ChatWindow:
    def __init__(self, master, usernameString):
        self.master = master
        frame = Frame(master)
        frame.pack()
        self.alias = usernameString

        self.titleMessage = Label(frame, text="Welcome to Global Chat " + usernameString + "!")
        self.chatBox = Text(frame, height=10)
        self.textInput = Entry(frame)
        self.textSubmit = Button(frame, text="Send")
        self.textSubmit.bind("<Button-1>", self.submitMessage)
        self.master.bind('<Return>', self.submitMessage)
        self.logoutBtn = Button(frame, text= "Logout and Exit Window")
        self.logoutBtn.bind("<Button-1>", self.logoutUser)

        self.titleMessage.grid(row=0)
        self.logoutBtn.grid(row=0, column=1, sticky = W + E)
        self.chatBox.grid(row=1, columnspan=2)
        self.textInput.grid(row=2, sticky=W + E)
        self.textSubmit.grid(row=2, column=1, sticky=E + W)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((host, port))
        self.s.setblocking(0)

        self.rT = threading.Thread(target=self.receving, args=("RecvThread", self.s))
        self.rT.start()

        print(self.alias)

    def logoutUser(self, event):
        self.master.destroy()
        '''
            TODO find a way to insert the following code and exit the window
            shutdown = True
            rT.join()
            s.close()
        '''

    def submitMessage(self, event):
        print("submitMessage function accessed")
        message = self.textInput.get()
        self.s.sendto(self.alias + ": " + message, server)
        print(self.alias + ": " + message, server)
        self.textInput.delete(0, 'end')

    def receving(self, name, sock):
        print("thread start")
        while not shutdown:
            try:
                tlock.acquire()
                while True:
                    data, addr = sock.recvfrom(1024)
                    print(str(data) + " hi")

                    self.chatBox.insert(INSERT, str(data) + "\n", server)
            except:
                pass
            finally:
                tlock.release()


def main():
    root = Tk()
    client = LoginWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()