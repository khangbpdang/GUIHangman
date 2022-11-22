#!/usr/bin/python
import random
from tkinter import *
"""
words=[ "minimize", "apple", "thanksgiving", "hyperbole", "creampuff", "quiet",
    "networking", "cybersecurity" ]
"""

words = ["australia", "austria", "azerbaijan", "china", "vietnam", "cuba", "guyana", "iran", "iraq", "italy", "spain", "belgium", "canada", "Albania", "Algeria", "Andorra", "Angola"]

ensure = []
class hangman:

    def __init__(self):
        """ Create a new game. Choose a word randomly from the list of possible
            words and set it as the target of the game. Initialize the turn
            counter to 0. Initialize guessed (total list of guest chars) and correct
            (list of correct guesses) to empty lists.
        """
        self.turns = 10
        self.guessed = []
        self.correct = []
        self.target = words[random.randrange(len(words))].lower()
        ensure.append(self.target) # list of words already used
        
    def getStatus(self):
        """ Returns a list of characters containing the word. Correctly guessed characters
        will be unmasked. Unguessed chars will be masked """
        out=[]
        for c in self.target:
            if c in self.guessed:
                out.append(c)
            elif c == " ":
                out.append(" ")
            elif c == "-":
                out.append("-")
            else:
                out.append("_")
        return " ".join(out).upper()
        
    def guess(self, choice):
        # guess if choice is in the target
        """
        if choice in self.guessed:
            return self.turns

        self.guessed.append(choice)
        if choice in self.target:
            self.correct.append(choice)
        else:
            self.turns -= 1
        """
        if (choice.isdigit() == True): # player cannot enter a number
            return "Please re-enter a character not a number."
            
        if (len(choice) != 1): # player cannot enter more than 1 character
            return "Please re-enter a character."

        if choice.lower() in self.guessed: # player cannot enter a previous valid input
            return "The character " + "\'" + choice.upper() + "\'" + " is already in previous guesses."

        # turning the game into a case-insensitive one
        self.guessed.append(choice.lower()) # save the letter input in lowercase
        if choice.lower() in self.target:
            self.correct.append(choice.upper()) # save the correct letter in uppercase
        else:
            self.turns -= 1
        
    def turnsLeft(self):
        return self.turns

    def won(self):
        return not '_' in self.getStatus()

    def getGuessed(self): # method to print out the guessed letters
        if (len(ensure) != 0):
            self.guessed.sort()
            return "Words used: " + ", ".join(self.guessed).upper()
        else:
            return

    def getTarget(self): # return the word the player is supposed to guess
        return self.target

SIZEX = 350
SIZEY = 125
COLUMNSPAN = 5
WINSIZEX = 700
WINSIZEY = 700
class HangmanGUI:
    def __init__(self, game):
        """ draw the GUI """
        self.game = game
        
        # TODO
        # build out the GUI, place all components, and register
        # the callback functions
        window = Tk() # main window
        window.minsize(width=WINSIZEX, height=WINSIZEY)
        window.configure(bg = "turquoise", cursor = "spider")
        window.title("Welcome To The Hangman Game !!!")
        
        self.windowLabel = StringVar() # window label
        self.windowLabel.set("HANGMAN")
        Label(window, fg = "purple", textvariable = self.windowLabel, font = ("Verdana", 30), bg = "turquoise").grid(row = 0, column = 0, columnspan = COLUMNSPAN)

        self.status = StringVar() # status label to report the status of the game to the player
        self.status.set(game.getStatus())
        Label(window, textvariable = self.status, height = 5, font=(26), bg = "turquoise", fg = "red").grid(row = 1, column = 0, columnspan = COLUMNSPAN)

        self.yourguess = Label(window, text = "Enter your guess:", fg = "orange red", bg = "turquoise") # Enter your guess:
        self.yourguess.grid(row = 2, column = 0, columnspan = 1, sticky = W+E+N+S)

        self.update = StringVar() # return the words already used by player
        Label(window, textvariable = self.update, bg = "turquoise").grid(row = 3, column = 0, columnspan = COLUMNSPAN)
        window.rowconfigure(3, min = 50)
        
        self.announce = StringVar() # announce whether the player wins or lose
        self.announce.set("")
        Label(window, textvariable = self.announce, font = ("Helvetica", 30), bg = "turquoise").grid(row = 4, column = 0, columnspan = COLUMNSPAN)
        window.rowconfigure(3, min = 50)
        
        self.entry = Entry(window, bg = "light goldenrod") # user input field
        self.entry.bind('<Return>', self.enter2Cmd) # register enter keystroke as an enter button
        self.entry.grid(row = 2, column = 1, columnspan = 1, sticky = W+E+N+S)

        self.enterButton = Button(window, text = "ENTER", command = self.enterCmd, activebackground = 'black', activeforeground = "mediumspringgreen")
        self.enterButton.grid(row = 2, column = 2, columnspan = 1, sticky = W+E+N+S) # button to enter words

        self.resetButton = Button(window, text = "RESET", command = self.reset, activebackground = 'lightcoral', activeforeground = "yellow")
        self.resetButton.grid(row = 2, column = 3, columnspan = 1, sticky = W+E+N+S) # button to reset the game and get new words

        self.rageQuitButton = Button(window, text = "I GIVE UP!", command = self.giveUp, activebackground = 'lightgoldenrod1', activeforeground = "lightslateblue")
        self.rageQuitButton.grid(row = 2, column = 4, columnspan = 1, sticky = W+E+N+S) # button to end the game early without further guessing

        self.canvas = Canvas(window , width = WINSIZEX, height = WINSIZEY - 200) # canvas to draw hangman
        self.canvas.grid(row = 5, column = 0, columnspan = 5, sticky=E+W+N+S)

        window.mainloop()

    def reset(self): # resets in game by loading a new word.
        self.game.__init__()
        while self.game.getTarget() != ensure[len(ensure)-1]: #reset the game if new word matches previous word
            self.game.__init__()
        self.status.set(game.getStatus())
        self.status.get()
        self.update.set("A NEW GAME HAS JUST STARTED.")
        self.announce.set("")

        # enable buttons and text input fields
        self.entry.config(state=NORMAL)
        self.rageQuitButton.config(state = NORMAL)
        self.enterButton.config(state = NORMAL)

        self.canvas.delete("all") # clear the canvas

    def enter2Cmd(self, event): # enter keystroke registration
        self.enterCmd()
        
    def enterCmd(self): # enter button operation - print hangman, print whether the player win or lose 
        x = self.game.guess(self.entry.get())        
        if x != None:
            self.update.set(x + "\n" + self.game.getGuessed())
            self.entry.delete(0, END)
            return
        #if x == self.game.turnsLeft():
        #elif
        if not self.game.won():
            self.drawHangman(self.game.turnsLeft())
            if game.turnsLeft() != 0:
                self.update.set("You have just entered: " + self.entry.get().upper() + ". There are " + str(self.game.turnsLeft()) + " turn(s) left.\n" + self.game.getGuessed())
                self.status.set(game.getStatus())
                self.status.get()
                self.entry.delete(0, END) # clear text field after every input            
            else:
                self.entry.delete(0, END)
                self.update.set("The word is " + self.game.getTarget().upper() + ".\nThe game has ended. Please press RESET to begin a new game.")
                self.announce.set("GAME OVER! YOU LOSE!")

                #disable buttons but the reset button if player wins
                self.entry.config(state=DISABLED)
                self.enterButton.config(state = DISABLED)
                self.rageQuitButton.config(state = DISABLED)
        else:
            self.status.set(game.getStatus())
            self.status.get()
            self.entry.delete(0, END)
            self.update.set("The word is " + self.game.getTarget().upper() + ".\nThe game has ended. Please press RESET to begin a new game.")
            self.announce.set("CONGRATULATIONS! YOU GUESS\n CORRECTLY THE WORD.")
            
            #disable buttons but the reset button if player loses
            self.entry.config(state=DISABLED)
            self.enterButton.config(state = DISABLED)
            self.rageQuitButton.config(state = DISABLED)

    def giveUp(self): # prints the correct word, print the hangman and end the game
        self.update.set("The word is " + self.game.getTarget().upper() + ". The game has ended. Please press RESET to begin a new game.")
        self.announce.set("SHAME ON YOU! BOO")
        self.entry.delete(0, END)
        
        # disable enter button and give up button after giving up
        self.entry.config(state=DISABLED)
        self.rageQuitButton.config(state = DISABLED)
        self.enterButton.config(state = DISABLED)
        for i in range(0,10):
            self.drawHangman(i)
        

    def drawHangman(self, turn): # draw hangaman based on an integer parameter
        if turn == 9:
            self.canvas.create_line(SIZEX-125, SIZEY+300, SIZEX+100, SIZEY+300) # ground
        elif turn == 8:
            self.canvas.create_line(SIZEX-100, SIZEY+300, SIZEX-100, SIZEY-50) # pole
        elif turn == 7:
             self.canvas.create_line(SIZEX-100, SIZEY-50, SIZEX+50, SIZEY-50) # horizontal bar
        elif turn == 6:
             self.canvas.create_line(SIZEX+50, SIZEY-50, SIZEX+50, SIZEY) # rope
        elif turn == 5:
            self.canvas.create_oval(SIZEX, SIZEY, SIZEX+100, SIZEY+100) # head
        elif turn == 4:
            self.canvas.create_line(SIZEX+50, SIZEY+100, SIZEX+50, SIZEY+175) # body
        elif turn == 3:
            self.canvas.create_line(SIZEX+50, SIZEY+175, SIZEX, SIZEY+250) # left leg            
        elif turn == 2:
              self.canvas.create_line(SIZEX+50, SIZEY+175, SIZEX+100, SIZEY+250) # right leg
        elif turn == 1:    
            self.canvas.create_line(SIZEX+20, SIZEY+140, SIZEX+80, SIZEY+140) # arms
        elif turn == 0:
            self.canvas.create_line(SIZEX+22.5, SIZEY+22.5, SIZEX+39.5, SIZEY+39.5) # left eye
            self.canvas.create_line(SIZEX+22.5, SIZEY+39.5, SIZEX+39.5, SIZEY+22.5)
                
            self.canvas.create_line(SIZEX+67.5, SIZEY+22.5, SIZEX+84.5, SIZEY+39.5) # right eye
            self.canvas.create_line(SIZEX+67.5, SIZEY+39.5, SIZEX+84.5, SIZEY+22.5)
                
            self.canvas.create_arc(SIZEX+25, SIZEY+60, SIZEX+75, SIZEY+83, style = ARC, extent = 180) # mouth
            self.canvas.create_arc(SIZEX+30, SIZEY+48, SIZEX+40, SIZEY+76, style = ARC, extent = -165) #tongue
        else:
            return "___ERROR___"
            
if __name__ == "__main__":
    random.seed()
    game = hangman()
    gui = HangmanGUI(game)
