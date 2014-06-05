import sys
#try:
#from tkinter import *
#except:
#	from Tkinter import *

class Stdin(object):
	def __init__(self):
		self.root = Tk()
		self.root.title("Stdin Input for Run Plugin")

		self.root.geometry("400x100")

		self.root.configure(background="#333")


		self.label = Label(text="Insert the stdin here")
		self.label.pack(pady=5)
		self.label.configure(background="#333")

		self.entry = Entry(self.root, width=300)
		self.entry.pack(padx=20,pady=0)
		self.entry.focus()

		# here is the application variable
		self.contents = StringVar()
		# set it to some value
		self.contents.set("")
		# tell the entry widget to watch this variable
		self.entry["textvariable"] = self.contents

		# and here we get a callback when the user hits return.
		self.entry.bind('<Key-Return>', self.destroy_key)

		b = Button(self.root, text="OK", command=self.destroy_button).pack(side="bottom")

		mainloop()

	def destroy_button(self):
		self.root.destroy()

	def destroy_key(self,event):
		self.root.destroy()

	def getString(self):
		print(self.contents.get())


#st = Stdin()
#st.getString()