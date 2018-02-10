from tkinter import *

root = Tk()

titleMessage = Label(root, text="Welcome to Global Chat!")
chatBox = Text(root, height=10)
textInput = Entry(root)
textSubmit = Button(root, text = "Send")

titleMessage.grid(row=0, columnspan = 2)
chatBox.grid(row=1, columnspan = 2)
textInput.grid(row=2, sticky=W+E)
textSubmit.grid(row=2, column=1, sticky=E+W)


root.mainloop()
