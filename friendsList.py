from Tkinter import *

root = Tk()


titleMessage = Label(root, text="Friend's List")
usernameMessage = Label(root, text="Hello User!")
globalChatBtn = Button(root, text = "Enter Global Chat")
privateChatBtn = Button(root, text = "Chat Selected Friend")
scrollbar = Scrollbar(root)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
logoutBtn = Button(root, text = "Logout")
addFriendBtn = Button(root, text = "Add Friend")


titleMessage.grid(row=0, columnspan = 2)
usernameMessage.grid(row=1, columnspan = 2)
logoutBtn.grid(row=2, sticky = E+W, columnspan = 2)
scrollbar.grid(row=3, column=1, sticky= N+S)
listbox.grid(row=3, column=0)
scrollbar.config(command=listbox.yview)
privateChatBtn.grid(row=4, sticky = E+W, columnspan = 2)
globalChatBtn.grid(row=5, sticky = E+W, columnspan = 2)
addFriendBtn.grid(row=6, sticky = E+W, columnspan = 2)

print(listbox.size())

def addFriend(event):
    friendName = raw_input("Enter Friend name: ")
    print(friendName)
    listbox.insert(END, friendName)

def selectFriend(event):
    if listbox.size() == 0:
        print("There are no friends available!")
    else:
        selectedFriend = listbox.get(listbox.curselection())
        print(selectedFriend)

addFriendBtn.bind("<Button-1>", addFriend)
listbox.bind("<<ListboxSelect>>", selectFriend)



root.mainloop()
