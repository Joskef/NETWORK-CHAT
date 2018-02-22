from tkinter import *

root = Tk()

# Hello from brigs

titleMessage = Label(root, text="Enter Username")
textInput = Entry(root)
textSubmit = Button(root, text = "Login")

titleMessage.grid(row=0)
textInput.grid(row=1, sticky=W+E)
textSubmit.grid(row=2, sticky=E+W)


root.mainloop()