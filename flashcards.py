from tkinter import *
from tkinter import messagebox
import random

def generate(path): # function for generating a dictionary of flashcards from a text file
	try:
		f=open(path,"r") # open the file
		lines=[] # init lines array
		for l in f: # for each line in the file
			line=l.rstrip() # strip the line of blank chars
			if line: # if the line is not blank
				lines.append(line) # append it to list of lines
		q=[] # init questions arr
		a=[] # init answers arr
		for i,line in enumerate(lines,1): # for each line in lines with index i
			if i%2!=0: # if odd
				q.append(line) # its a question so add it to q
			else:
				a.append(line) # its an answer so add it to a

		flashcards={} # init flashcards
		for x in range(0,len(q)): # for as long as q (which should be as long as a)
			flashcards.update({q[x]:a[x]}) # put qs and as together in dict

		return flashcards # return
	except IndexError: # if the text file has uneven lines
		return "error"
	except FileNotFoundError: # if the text file doesn't exist
		return "error2"

def format(master): # procedure for formatting windows and widgets easily
	master.configure(bg=bgcolor) # master will be the window
	for w in master.winfo_children(): # for every widget in the window
		name=w.winfo_class() # get the type of widget (button, label, etc.)
		if name=="Radiobutton" or name=="Button" or name=="Label" or name=="LabelFrame": # if its any of these three
			w.configure(bg=bgcolor,fg=fgcolor) # set bg and fg colors
		if name=="Frame": # if its a frame
			w.configure(bg=bgcolor) # set the bg color
		if name=="Button" or name=="Radiobutton": # if its a button or radiobuttons
			w.configure(activebackground=bgcolor,activeforeground=fgcolor,cursor="hand2") # set active colors
		if name=="Radiobutton": # if its a radiobutton
			w.configure(selectcolor=bgcolor) # set the selector (white bit) color

def center(win): # procedure for centering window
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
# thank you: https://stackoverflow.com/questions/3352918/how-to-center-a-window-on-the-screen-in-tkinter

def main(cards): # main flashcards window procedure
	def showhide(answer,textvar): # sub procedure to toggle show/hide on button click
		if textvar.get()=="???": # if the answer is hidden, show it
			textvar.set(answer)
		else: # if the answer is shown, hide it
			textvar.set("???")
		format(main)

	def goback(): # procedure for go back button
		main.destroy() # destroy this window
		menu() # start menu

	main=Tk() # generate tkinter window
	main.geometry("+500+300") # set position of window
	main.title("Flashcards") # set title of window
	main.resizable(0,0) # prevent user from resizing window

	r,c=0,0 # init row/column variables
	for q in cards: # for question in cards
		lftext="Question {}".format(list(cards).index(q)+1) # question number label for labelframe
		lf=LabelFrame(main,text=lftext) # create labelframe to contain current card
		lf.grid(row=r,column=c,padx=5,pady=5,sticky="nesw") # grid the labelframe
		qLabel=Label(lf,text=q,wraplength=200) # create question labels
		qLabel.grid(sticky="nesw") # grid question labels
		textvar=StringVar() # use answer as stringvar for ease when switching
		textvar.set("???") # set answers to hidden at first
		aLabel=Label(lf,textvariable=textvar,wraplength=200) # create answer labels
		aLabel.grid(sticky="nesw") # grid answer labels
		a=cards[q] # set current answer to a
		sButton=Button(lf,text="show/hide",command=lambda a=a,textvar=textvar:showhide(a,textvar)) # button to show/hide answers
		sButton.grid(sticky="nesw",padx=5,pady=5) # grid show/hide button
		c+=1
		if c>round(len(cards)/4):
			c=0
			r+=1
		format(lf) # set the labelframe colors

	backb=Button(main,text="Go back",command=goback) # button to go back to start screen
	backb.grid(columnspan=10,sticky="nesw") # grid back button

	format(main) # set the main window colors
	center(main) # center main window

	main.mainloop() # keep window loop running

def menu(): # initial menu procedure
	def go(): # go button click sub procedure
		global e,lb # need to global entry and listbox widgets to access their contents
		val=v.get() # store the user's selection from radio buttons

		if val==0: # if they picked 'show all'
			cards=generate(path)  # easy, just generate a dictionary of all the cards :)
		elif val==1: # if they picked 'random selection'
			c=generate(path) # get all flashcards and store them in c
			num=int(e.get()) # get the number of flashcards they specified in spinbox
			cards={} # init empty cards dictionary
			for x in range(0,num): # for as many flashcards the user specified
				randq=random.choice(list(c)) # pick a random card
				while randq in cards: # if its already been picked, pick again until its unique
					randq=random.choice(list(c))
				cards.update({randq:c[randq]}) # update the cards dict with the chosen card
		elif val==2: # if they picked 'pick own'
			c=generate(path) # get all cards for querying
			cards={} # init blank cards dict
			for sel in lb.curselection(): # for every selection the user made
				q=lb.get(sel) # get the question and store it in q
				a=c[q] # get the answer from c dict
				cards.update({q:a}) # update cards dict with question and answer
		root.destroy() # close this window, since we're done
		main(cards) # now the cards are selected, call the main window procedure

	def update(): # update sub procedure
		global e,lb # we need to global the spinbox and listbox for go procedure

		for w in optionFrame.winfo_children(): # we need to clear out the frame so we arent stacking widgets
			w.destroy()

		val=v.get() # get the user's radiobutton choice

		if val==0: # if they picked 'show all'
			pass # explicitly do nothing to avoid confusion. there are no extra options
		elif val==1: # if they picked 'random selection'
			l=Label(optionFrame,text="Number of cards to generate") # create a label asking how many to choose
			l.grid() # grid label
			e=Spinbox(optionFrame,from_=1,to=len(generate(path)),state="readonly") # create spinbox for int choice
			e.grid() # grid spinbox
		elif val==2: # if they picked 'pick own'
			l=Label(optionFrame,text="Choose questions") # label instruction for user
			l.grid(row=0,column=0)
			cards=generate(path) # get all cards stored in cards
			scrollbar=Scrollbar(optionFrame) # scroll bar for touch pad users :)
			scrollbar.grid(row=1,column=1,sticky="ns",rowspan=5) # grid scrollbar
			lb=Listbox(optionFrame,yscrollcommand=scrollbar.set,selectmode=MULTIPLE) # listbox containing all card questions
			lb.grid(row=1,column=0,rowspan=5) # grid listbox
			scrollbar.config(command=lb.yview) # map listbox's scroll to scrollbar
			for q in cards: # for question in cards
				lb.insert(END,q) # insert the question into the listbox

		format(optionFrame) # call to window formatting procedure

	root=Tk() # create root window
	root.geometry("400x300+500+300") # set size and position of window
	root.title("Flashcards") # set title of window
	root.resizable(0,0) # prevent user from resizing window

	test=generate(path) # try generating flashcards to make sure the file is valid
	if test=="error": # if the text file is invalid show an error
		error=messagebox.showerror("Error","Text file contains uneven number of question/answer lines")
		root.destroy() # close the window
	elif test=="error2": # if the text file doesnt exist show an error
		error=messagebox.showerror("Error","Make sure there is a 'flashcards.txt' file in the same folder as this program")
		root.destroy() # close the window
	else:
		modes=[("Show all",0),("Random selection",1),("Pick own",2)] # user options for selecting cards
		v=IntVar() # the user's choice is stored as an intvar
		v.set(0) # set the default choice to 0 (show all)
		r,c=0,0
		for mode,value in modes: # for each mode
			b = Radiobutton(root, text=mode,variable=v,value=value,command=update) # create a radio button widget
			b.grid(row=r,column=c,sticky="w",padx=10,pady=25) # grid the radio buttons
			r+=1

		optionFrame=Frame(root) # a frame to hold further options depending which mode the user chooses
		optionFrame.grid(row=0,column=1,rowspan=4,padx=10,pady=10) # grid the frame
		update() # function to refresh the option frame according to the choice made

		sButton=Button(root,text="Go",command=go) # submit 'go' button to affirm all choices
		sButton.grid() # grid the go button

	format(root) # call to window formatting procedure
	center(root) # call to center window on screen

	root.mainloop() # keep root window running

path="flashcards.txt" # path to flashcards text
bgcolor="#aea6ea" # global background color
fgcolor="#000000" # global foreground color
menu() # start
