from tkinter import *
from tkinter import messagebox
import random

def generate(path):
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
	except IndexError: # if the text file is invalid return error
		return "error"
	except FileNotFoundError:
		return "error2"

def main():
	def show(card,t): # function to toggle show/hide
		if t.get()=="???": # if its hidde then show it
			t.set(card)
		else: # if its shown then hide it
			t.set("???")
			
	root=Tk() # generate tkinter window
	
	cards=generate("flashcards.txt") # generate cards
	if cards=="error": # if the text file is invalid show an error
		error=messagebox.showerror("Error","Text file contains uneven number of question/answer lines")
		root.destroy() # close the window
	elif cards=="error2": # if the text file doesnt exist show an error
		error=messagebox.showerror("Error","Make sure there is a 'flashcards.txt' file in the same folder as this program")
		root.destroy() # close the window
	else:
		if len(cards)>6: # if there are more than 6 cards we can pick some random cards
			newcards={} # make a new dict for the random choices
			for x in range(0,5): # iterate 6 times
				randq=random.choice(list(cards)) # pick a question
				while randq in newcards: # if it picks one already picked, pick again until a fresh one is chosen
					randq=random.choice(list(cards)) # set randq to the question
				ans=cards[randq] # get the answer and store it in ans
				newcards.update({randq:ans}) # update newcards
		else:
			newcards=cards # if there are less than 6, just use all of them
				
		for key in newcards: # for each card
			qLabel=Label(root,text=key) # create question labels
			qLabel.grid() # grid question labels
			t=StringVar() # use answer as stringvar for ease when switching
			t.set("???") # set answers to hidden at first
			aLabel=Label(root,textvariable=t) # create answer labels
			aLabel.grid() # grid answer labels
			c=newcards[key] # set current answer to c
			sButton=Button(root,text="show/hide",command=lambda c=c,t=t:show(c,t)) # button to show/hide answers
			sButton.grid() # grid show/hide button
		
		root.mainloop() # keep window loop running
	

main() # start
