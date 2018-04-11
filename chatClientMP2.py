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
            self.client = MainWindow(self.newWindow, tempUserString)  # create new window and pass the new username string to the new window


class MainWindow:
    def __init__(self, master, usernameString):
        self.master = master
        frame = Frame(master)
        frame.pack()
        self.usernameString = usernameString
        self.chatRecipientNum = 0;
        self.chatRoomID = 0;
        self.shutdown = False
        self.clientNumber = self.getClientNumber();
        self.messageType = "gm"

        # GUI initialization

        self.welcomeUserMessage = Label(frame, text="Welcome " + str(self.clientNumber) + " "+ self.usernameString + "!")
        self.userListTitle = Label(frame, text="Online Users")
        self.chatroomTitle = Label(frame, text="Chat Rooms")
        self.chatBox = Text(frame, height=10)
        self.chatInput = Entry(frame)
        self.chatSubmitBtn = Button(frame, text="Send")
        self.logoutBtn = Button(frame, text="Logout")
        self.createChatRoomBtn = Button(frame, text="Join Chat Room 1")
        self.createChatRoom2Btn = Button(frame, text="Join Chat Room 2")
        self.createChatRoom3Btn = Button(frame, text="Join Chat Room 3")
        self.createGroupChatBtn = Button(frame, text="Invite to Group Chat")
        self.enterGlobalChatBtn = Button(frame, text="Enter Global Chat Mode")
        self.enterPrivateChatBtn = Button(frame, text="Enter Private Chat Mode")
        self.enterFileTransferBtn = Button(frame, text="Enter File Transfer Mode")
        self.createGroupChatInput = Entry(frame)

        self.fileSendLabel = Label(frame, text="Enter File to Upload")
        self.fileDownloadLabel = Label(frame, text="Enter File to Download")
        self.fileSendInput = Entry(frame)
        self.fileDownloadInput = Entry(frame)
        self.fileSendBtn = Button(frame, text="Upload")
        self.fileDownloadBtn = Button(frame, text="Download")

        self.chatRoomPasswordLabel = Label(frame, text = "Enter Chatroom Password")
        self.chatRoomPasswordInput = Entry(frame)
        self.chatRoomPasswordBtn = Button(frame, text = "Submit")
        self.chatRoomPasswordFeedback = Label(frame)

        # For Users list
        self.scrollbarUsers = Scrollbar(frame)
        self.listboxUsers = Listbox(frame, yscrollcommand=self.scrollbarUsers.set)


        self.userListTitle.grid(row=0, column=0, columnspan=2)
        self.listboxUsers.grid(row=1, column=0)
        self.scrollbarUsers.grid(row=1, column=1, sticky=N + S)
        self.chatroomTitle.grid(row=2, column=0, columnspan=2)
        self.welcomeUserMessage.grid(row=0, column=3)
        self.chatBox.grid(row=1, column=3, rowspan=6, columnspan=3, sticky=N + S)
        self.chatInput.grid(row=7, columnspan=2, column= 3, rowspan=2, sticky=N + S + W + E)
        self.chatSubmitBtn.grid(row=7, column=5, rowspan=2, sticky=N + S + W + E)
        self.createChatRoomBtn.grid(row=5, columnspan=2, sticky=W + E)
        self.createChatRoom2Btn.grid(row=6, columnspan=2, sticky=W + E)
        self.createChatRoom3Btn.grid(row=7, columnspan=2, sticky=W + E)
        self.logoutBtn.grid(row=0, column=5, sticky=E)
        self.enterPrivateChatBtn.grid(row=9, columnspan=2, sticky=W +E)
        self.enterGlobalChatBtn.grid(row=10, columnspan=2, sticky=W + E)
        self.createGroupChatInput.grid(row=11, columnspan=2, sticky=W + E)
        self.createGroupChatBtn.grid(row=12, columnspan=2, sticky=W + E)
        #self.enterFileTransferBtn.grid(row=9, columnspan=2, sticky=W + E)

        # For File Transfer Mode

        self.fileSendLabel.grid(row=9, column=3, sticky=W + E)
        self.fileSendInput.grid(row=9, column=4, sticky=W + E)
        self.fileSendBtn.grid(row=9, column=5, sticky=W + E)
        self.fileDownloadLabel.grid(row=10, column=3, sticky=W + E)
        self.fileDownloadInput.grid(row=10, column=4, sticky=W + E)
        self.fileDownloadBtn.grid(row=10, column=5, sticky=W + E)

        # For Chat Room Mode

        self.chatRoomPasswordLabel.grid(row=11, column=3, sticky=W + E)
        self.chatRoomPasswordInput.grid(row=11, column=4, sticky=W + E)
        self.chatRoomPasswordBtn.grid(row=11, column=5, sticky=W + E)
        self.chatRoomPasswordFeedback.grid(row=12, column=3, columnspan=3, sticky=W + E)


        # config and binds
        # self.chatBox.config(state = DISABLED)
        self.master.bind('<Return>', self.submitMessageGlobalChat)
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageGlobalChat)
        self.listboxUsers.bind("<<ListboxSelect>>", self.chatPrivateUser)
        self.enterPrivateChatBtn.config(state=DISABLED)
        self.enterGlobalChatBtn.bind('<Button-1>', self.initGlobalChatMode)
        self.createGroupChatBtn.bind('<Button-1>', self.initGroupChatMode)
        self.fileDownloadBtn.bind('<Button-1>', self.downloadFromFileServer)
        self.createChatRoomBtn.bind('<Button-1>', self.initChatRoomMode1)
        self.createChatRoom2Btn.bind('<Button-1>', self.initChatRoomMode2)
        self.createChatRoom3Btn.bind('<Button-1>', self.initChatRoomMode3)

        self.chatRoomPasswordLabel.config(state=DISABLED)
        self.chatRoomPasswordInput.config(state=DISABLED)
        self.chatRoomPasswordBtn.config(state=DISABLED)
        self.chatRoomPasswordFeedback.config(state=DISABLED)

        self.chatRoomPasswordBtn.bind('<Button-1>', self.joinChatRoom)






        # server stuff
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #group and private chat
        self.s.bind((host, port))
        self.s.setblocking(0)

        self.skClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #fileTransfer
        self.skClient.connect(("127.0.0.1", 2525))
        self.sData = "Temp"

        self.rT = threading.Thread(target=self.receiving, args=("RecvThread", self.s))
        self.rT.start()

        self.s.sendto(self.usernameString, server)
        self.s.sendto("has joined the Global Chat!", server)


        self.logoutBtn.bind('<Button-1>', self.submitLogout)

    def submitLogout(self, event):
        self.shutdown = True
        self.rT.join()
        self.s.close()

    def initPrivateChatMode(self, event):
        self.chatBox.delete(1.0, END) #clear text area
        self.chatBox.insert(INSERT, "Welcome to Private Chat Mode!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessagePrivateChat)
        self.master.bind('<Return>', self.submitMessagePrivateChat)

    def initGlobalChatMode(self, event):
        self.chatBox.delete(1.0, END) #clear text area
        self.chatBox.insert(INSERT, "Welcome to Global Chat Mode!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageGlobalChat)
        self.master.bind('<Return>', self.submitMessageGlobalChat)

    def initGlobalChatModeNonEvent(self):
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Welcome to Global Chat Mode!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageGlobalChat)
        self.master.bind('<Return>', self.submitMessageGlobalChat)

    def initGroupChatMode(self, event):
        print("createGroupChatInput = " + str(self.createGroupChatInput.get()))
        self.addToGroupChat(self.createGroupChatInput.get())  # invite client num to group chat
        #self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Welcome to Group Chat Mode!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageGroupChat)
        self.master.bind('<Return>', self.submitMessageGroupChat)

    def initChatRoomMode1(self, event):
        self.chatRoomID = 1
        self.addToPrivateChat(self.clientNumber)  # join chat room chat
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Please Enter Password for Chat Room 1\n")
        self.chatRoomPasswordLabel.config(state=NORMAL)
        self.chatRoomPasswordInput.config(state=NORMAL)
        self.chatRoomPasswordBtn.config(state=NORMAL)
        self.chatRoomPasswordFeedback.config(state=NORMAL, text="Please Enter Chatroom Password")


    def initChatRoomMode2(self, event):
        self.chatRoomID = 2
        self.addToPrivateChat2(self.clientNumber)  # join chat room chat
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Please Enter Password for Chat Room 2\n")
        self.chatRoomPasswordLabel.config(state=NORMAL)
        self.chatRoomPasswordInput.config(state=NORMAL)
        self.chatRoomPasswordBtn.config(state=NORMAL)
        self.chatRoomPasswordFeedback.config(state=NORMAL, text="Please Enter Chatroom Password")


    def initChatRoomMode3(self, event):
        self.chatRoomID = 3
        self.addToPrivateChat3(self.clientNumber)  # join chat room chat
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Please Enter Password for Chat Room 3\n")
        self.chatRoomPasswordLabel.config(state=NORMAL)
        self.chatRoomPasswordInput.config(state=NORMAL)
        self.chatRoomPasswordBtn.config(state=NORMAL)
        self.chatRoomPasswordFeedback.config(state=NORMAL, text="Please Enter Chatroom Password", fg = "black")


    def joinChatRoom(self, event):
        if(self.chatRoomID == 1):
            if(self.chatRoomPasswordInput.get() == "pc1"):
                self.chatRoomPasswordFeedback.config(text="Private Chat 1 Accessed!", fg = "dark green")
                self.beginChatRoomMode()
            else:
                self.chatRoomPasswordFeedback.config(text="Invalid Password. Unauthorized Private Chat 1 Access! Returning to Global Chat.", fg="red")
                self.initGlobalChatModeNonEvent()
        elif(self.chatRoomID == 2):
            if (self.chatRoomPasswordInput.get() == "pc2"):
                self.chatRoomPasswordFeedback.config(text="Private Chat 2 Accessed!", fg="dark green")
                self.beginChatRoomMode2()
            else:
                self.chatRoomPasswordFeedback.config(text="Invalid Password. Unauthorized Private Chat 2 Access! Returning to Global Chat.", fg="red")
                self.initGlobalChatModeNonEvent()
        elif (self.chatRoomID == 3):
            if (self.chatRoomPasswordInput.get() == "pc3"):
                self.chatRoomPasswordFeedback.config(text="Private Chat 3 Accessed!", fg="dark green")
                self.beginChatRoomMode3()
            else:
                self.chatRoomPasswordFeedback.config(text="Invalid Password. Unauthorized Private Chat 3 Access! Returning to Global Chat.", fg="red")
                self.initGlobalChatModeNonEvent()

    def beginChatRoomMode(self):
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Welcome to Chat Room 1!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageChatRoom)
        self.master.bind('<Return>', self.submitMessageChatRoom)

    def beginChatRoomMode2(self):
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Welcome to Chat Room 2!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageChatRoom2)
        self.master.bind('<Return>', self.submitMessageChatRoom2)

    def beginChatRoomMode3(self):
        self.chatBox.delete(1.0, END)  # clear text area
        self.chatBox.insert(INSERT, "Welcome to Chat Room 3!\n")
        self.chatSubmitBtn.bind('<Button-1>', self.submitMessageChatRoom3)
        self.master.bind('<Return>', self.submitMessageChatRoom3)

    def chatPrivateUser(self, event):
        self.enterPrivateChatBtn.config(state=NORMAL)
        self.enterPrivateChatBtn.bind("<Button-1>", self.initPrivateChatMode)
        self.chatRecipientNum = self.listboxUsers.curselection()[0] # get selected User's index in then convert to int
        self.chatBox.insert(INSERT, "You are chatting with " + str(self.chatRecipientNum) + "\n")
        print(self.chatRecipientNum)

    def downloadFromFileServer(self, event):
        self.sFileName = self.fileDownloadInput.get()
        print(self.sFileName)
        while True:
            self.skClient.send(self.sFileName)
            sData = self.skClient.recv(1024)
            fDownloadFile = open('new_' + self.sFileName, "wb")
            while sData:
                fDownloadFile.write(sData)
                sData = self.skClient.recv(1024)
            print "Download Completed"
            break

    def submitMessageChatRoom(self, event):
        self.messageType = "pc"
        print("submitMessageChatRoom function accessed")
        message = self.chatInput.get()
        #self.chatBox.insert(INSERT, self.usernameString + ": " + message +"\n")
        self.s.sendto("pc" + self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def submitMessageChatRoom2(self, event):
        self.messageType = "pc2"
        print("submitMessageChatRoom function accessed")
        message = self.chatInput.get()
        #self.chatBox.insert(INSERT, self.usernameString + ": " + message +"\n")
        self.s.sendto("pc2" + self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def submitMessageChatRoom3(self, event):
        self.messageType = "pc3"
        print("submitMessageChatRoom function accessed")
        message = self.chatInput.get()
        #self.chatBox.insert(INSERT, self.usernameString + ": " + message +"\n")
        self.s.sendto("pc3" + self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def submitMessageGroupChat(self, event):
        self.messageType = "gc"
        print("submitMessageGroupChat function accessed")
        message = self.chatInput.get()
        #self.chatBox.insert(INSERT, self.usernameString + ": " + message + "\n")
        self.s.sendto("gc" + self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def submitMessagePrivateChat(self, event):
        self.messageType = "pm"
        print("submitMessagePrivatChat function accessed")
        message = self.chatInput.get()
        self.chatBox.insert(INSERT, self.usernameString + ": " + message +"\n")
        self.s.sendto(str(self.chatRecipientNum) + "pm" + self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def submitMessageGlobalChat(self, event):
        self.messageType = "gm"
        print("submitMessageGlobalChat function accessed")
        message = self.chatInput.get()
        self.s.sendto("gm" + self.usernameString + ": " + message, server)
        print(self.usernameString + ": " + message, server)
        self.chatInput.delete(0, 'end')

    def addToGroupChat(self, clientIndex):
        print("self.addToGroupChat accessed")
        gcFileWrite = open("gc.csv", "a+")
        member = str(clientIndex) + "\n"
        gcFileWrite.write(member)
        gcFileWrite.close()

    def addToPrivateChat(self, clientIndex):
        pcFileWrite = open("pc.csv", "a+")
        member = str(clientIndex) + "\n"
        pcFileWrite.write(member)
        pcFileWrite.close()

    def addToPrivateChat2(self, clientIndex):

        pcFileWrite = open("pc2.csv", "a+")
        member = str(clientIndex) + "\n"
        pcFileWrite.write(member)
        pcFileWrite.close()

    def addToPrivateChat3(self, clientIndex):

        pcFileWrite = open("pc3.csv", "a+")
        member = str(clientIndex) + "\n"
        pcFileWrite.write(member)
        pcFileWrite.close()

    def getClientNumber(self):
        print("self.getClientNumber accessed")
        with open('info.csv') as fp:
            lines = fp.readlines()
            clientNumber = len(lines)
            print("getClientNumber returns " + str(clientNumber))
            return clientNumber

    def receiving(self, name, sock):
        print("thread start")
        while not shutdown or self.shutdown:
            try:
                tlock.acquire()
                while True:
                    data, addr = sock.recvfrom(1024)

                    if "gm" in data and "New User Entered!" not in data:
                        if self.messageType == "gm":
                            print(str(data[2:]))
                            self.chatBox.insert(INSERT, str(data[2:]) + "\n", server)

                    elif "New User Entered!" not in data:
                        print(str(data))
                        self.chatBox.insert(INSERT, str(data) + "\n", server)

                    client_names = f.readlines()
                    print "Client Names: \n"
                    for clientName in client_names:
                        print(clientName)
                        self.listboxUsers.insert(END, clientName )
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
