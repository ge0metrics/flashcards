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

def main(cards): # main flashcards window procedure
	def showhide(answer,textvar): # sub procedure to toggle show/hide on button click
		if textvar.get()=="???": # if the answer is hidden, show it
			textvar.set(answer)
		else: # if the answer is shown, hide it
			textvar.set("???")

	main=Tk() # generate tkinter window

	for q in cards: # for question in cards
		qLabel=Label(main,text=q) # create question labels
		qLabel.grid() # grid question labels
		textvar=StringVar() # use answer as stringvar for ease when switching
		textvar.set("???") # set answers to hidden at first
		aLabel=Label(main,textvariable=textvar) # create answer labels
		aLabel.grid() # grid answer labels
		a=cards[q] # set current answer to a
		sButton=Button(main,text="show/hide",command=lambda a=a,textvar=textvar:showhide(a,textvar)) # button to show/hide answers
		sButton.grid() # grid show/hide button

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
			l=Label(optionFrame,text="number of cards") # create a label asking how many to choose
			l.grid() # grid label
			e=Spinbox(optionFrame,from_=1,to=len(generate(path)),state="readonly") # create spinbox for int choice
			e.grid() # grid spinbox
		elif val==2: # if they picked 'pick own'
			cards=generate(path) # get all cards stored in cards
			scrollbar=Scrollbar(optionFrame) # scroll bar for touch pad users :)
			scrollbar.grid(row=0,column=1,sticky="ns") # grid scrollbar
			lb=Listbox(optionFrame,yscrollcommand=scrollbar.set,selectmode=MULTIPLE) # listbox containing all card questions
			lb.grid(row=0,column=0) # grid listbox
			scrollbar.config(command=lb.yview) # map listbox's scroll to scrollbar
			for q in cards: # for question in cards
				lb.insert(END,q) # insert the question into the listbox

	root=Tk() # create root window

	test=generate(path) # try generating flashcards to make sure the file is valid
	if test=="error": # if the text file is invalid show an error
		error=messagebox.showerror("Error","Text file contains uneven number of question/answer lines")
		root.destroy() # close the window
	elif test=="error2": # if the text file doesnt exist show an error
		error=messagebox.showerror("Error","Make sure there is a 'flashcards.txt' file in the same folder as this program")
		root.destroy() # close the window
	else:
		modes=[("show all",0),("random selection",1),("pick own",2)] # user options for selecting cards
		v=IntVar() # the user's choice is stored as an intvar
		v.set(0) # set the default choice to 0 (show all)
		for mode,value in modes: # for each mode
			b = Radiobutton(root, text=mode,variable=v,value=value,command=update) # create a radio button widget
			b.grid() # grid the radio buttons

		optionFrame=Frame(root) # a frame to hold further options depending which mode the user chooses
		optionFrame.grid() # grid the frame
		update() # function to refresh the option frame according to the choice made

		sButton=Button(root,text="go",command=go) # submit 'go' button to affirm all choices
		sButton.grid() # grid the go button

	root.mainloop() # keep root window running

path="flashcards.txt" # path to flashcards text
menu() # start
