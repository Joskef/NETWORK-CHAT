from Tkinter import *

root = Tk()

titleMessage = Label(root, text="Friend's List")
usernameMessage = Label(root, text="Hello User!")
globalChatBtn = Button(root, text = "Enter Global Chat")
privateChatBtn = Button(root, text = "Chat Selected Friend")
scrollbar = Scrollbar(root)
listbox = Listbox(root, yscrollcommand=scrollbar.set)
logoutBtn = Button(root, text = "Logout")

for i in range(50):
    listbox.insert(END, str(i))

titleMessage.grid(row=0, columnspan = 2)
usernameMessage.grid(row=1, columnspan = 2)
logoutBtn.grid(row=2, sticky = E+W, columnspan = 2)
scrollbar.grid(row=3, column=1, sticky= N+S)
listbox.grid(row=3, column=0)
scrollbar.config(command=listbox.yview)
privateChatBtn.grid(row=4, sticky = E+W, columnspan = 2)
globalChatBtn.grid(row=5, sticky = E+W, columnspan = 2)



root.mainloop()
