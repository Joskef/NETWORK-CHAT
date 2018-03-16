from Tkinter import *
import socket
import threading
import time
import pickle

VK_RETURN = 0x0D

tlock = threading.Lock()
shutdown = False

host = '127.0.0.1'
port = 0

f = open("info.csv", "r")

server = ('127.0.0.1', 5002)
message = 'New User Entered!'


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
            self.textFeedback.config(text="Please Enter a Username!", fg="red")
        else:
            tempUserString = 'null'
            tempUserString = self.textInput.get()
            self.textFeedback.config(text="Successfully logged in!", fg="dark green")
            self.newWindow = Toplevel(self.master)
            self.client = MainWindow(self.newWindow,
                                     tempUserString)  # create new window and pass the new username string to the new window


class MainWindow:
    def __init__(self, master, usernameString):
        self.master = master
        frame = Frame(master)
        frame.pack()
        self.usernameString = usernameString

        # GUI initialization

        self.welcomeUserMessage = Label(frame, text="Welcome " + self.usernameString + "!")
        self.userListTitle = Label(frame, text="Online Users")
        self.chatroomTitle = Label(frame, text="Chat Rooms")
        self.chatBox = Text(frame, height=10)
        self.chatInput = Entry(frame)
        self.chatSubmitBtn = Button(frame, text="Send")
        self.logoutBtn = Button(frame, text="Logout")
        self.createChatRoomBtn = Button(frame, text="Create Chat Room")
        self.createGroupChatBtn = Button(frame, text="Create Group Chat")

        # For Users list
        self.scrollbarUsers = Scrollbar(frame)
        self.listboxUsers = Listbox(frame, yscrollcommand=self.scrollbarUsers.set)

        # For Chatrooms list
        self.scrollbarChatrooms = Scrollbar(frame)
        self.listboxChatrooms = Listbox(frame, yscrollcommand=self.scrollbarChatrooms.set)

        self.userListTitle.grid(row=0, column=0, columnspan=2)
        self.listboxUsers.grid(row=1, column=0)
        self.scrollbarUsers.grid(row=1, column=1, sticky=N + S)
        self.chatroomTitle.grid(row=2, column=0, columnspan=2)
        self.listboxChatrooms.grid(row=3, column=0)
        self.scrollbarChatrooms.grid(row=3, column=1, sticky=N + S)
        self.welcomeUserMessage.grid(row=0, column=3)
        self.chatBox.grid(row=1, column=3, rowspan=3, columnspan=2, sticky=N + S)
        self.chatInput.grid(row=5, column=3, rowspan=2, sticky=N + S + W + E)
        self.chatSubmitBtn.grid(row=5, column=4, rowspan=2, sticky=N + S + W + E)
        self.createChatRoomBtn.grid(row=5, columnspan=2, sticky=W + E)
        self.createGroupChatBtn.grid(row=6, columnspan=2, sticky=W + E)
        self.logoutBtn.grid(row=0, column=4, sticky=E)

        # config and binds
        # self.chatBox.config(state = DISABLED)
        self.master.bind('<Return>', self.submitMessage)
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessage)

        # server stuff
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.bind((host, port))
        self.s.setblocking(0)

        self.rT = threading.Thread(target=self.receiving, args=("RecvThread", self.s))
        self.rT.start()

        self.s.sendto(self.usernameString, server)
	self.s.sendto("has joined the Global Chat!", server)

    def submitMessage(self, event):
        print("submitMessage function accessed")
        message = self.chatInput.get()
        self.s.sendto(self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def receiving(self, name, sock):
        print("thread start")
        while not shutdown:
            try:
                tlock.acquire()
                while True:
                    data, addr = sock.recvfrom(1024)
                    if "New User Entered!" not in data:
                        print(str(data))

                    self.chatBox.insert(INSERT, str(data) + "\n", server)
                    client_names = f.readlines()
                    print "Client Names: \n"
                    for clientName in client_names:
                        print(clientName)
                        self.listboxUsers.insert(END, clientName)
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
