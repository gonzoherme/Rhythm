from cmu_112_graphics import *
from tkinter import *
import time
from backend import *
from random import randint
import time
from PIL import Image, ImageTk, ImageSequence
import pygame
# import module_manager
# module_manager.review()


######################### BUTTONS ####################

class Button():
    def __init__(self, name, buttonNum, app, textColour, fill):
        self.name = name
        self.buttonNum = buttonNum
        self.text = name
        self.pressed = False
        self.fill = fill
        self.textColour = textColour

        
    def setSize(self, topLeftX, topLeftY, bottomRightX, bottomRightY):  
        # corner point coordinates
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY

        # center points
        self.centerButtonX = int((self.topLeftX + self.bottomRightX)/2)
        self.centerButtonY = int((self.topLeftY + self.bottomRightY)/2)


        # font
        self.fontSize = int(self.buttonNum*(self.centerButtonX/5))

        # # coordinates
        # self.coordinates = [self.topLeftX, self.topLeftY, self.bottomRightX, self.bottomRightY]


    def isPressed(self, event, app):
        # Button Changing State
        if (self.topLeftX < event.x < self.bottomRightX and
            self.topLeftY < event.y < self.bottomRightY):
            self.pressed = True
            self.fill = 'gray'
            print(self.fill)
        else:
            self.pressed = False
            self.fill = self.fill

           
        
    def draw(self, canvas):            
        # Draw rectangle
        canvas.create_rectangle(self.topLeftX, self.topLeftY,
                                self.bottomRightX, self.bottomRightY,
                                fill = self.fill)
        # Draw text
        canvas.create_text(self.centerButtonX, self.centerButtonY,
                           text = self.text,
                           fill = self.textColour,
                           font = f'Visby {self.fontSize} bold')
                


 
        
###################### SOUND PLAYING ################
# Citation: code obtained from cmu 112 Advanced Animations with Tkinter https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods
class Sound(object):
    def __init__(self, path):
        self.path = path
        self.loops = 1
        pygame.mixer.music.load(path)

    # Returns True if the sound is currently playing
    def isPlaying(self):
        return bool(pygame.mixer.music.get_busy())

    # Loops = number of times to loop the sound.
    # If loops = 1 or 1, play it once.
    # If loops > 1, play it loops + 1 times.
    # If loops = -1, loop forever.
    def start(self, loops=1):
        self.loops = loops
        pygame.mixer.music.play(loops=loops)

    # Stops the current sound from playing
    def stop(self):
        pygame.mixer.music.stop()
    



############# START MODE ###########################
def startMode_redrawAll(app, canvas):
    drawBackground(app, canvas, 'black')
    # Title
    canvas.create_text(app.width/2, app.height/10, text = 'rhythm', font = 'Visby 50 bold', fill = 'lightgreen')
    
    # Draw to competitive button
    app.buttonToCompetitive.draw(canvas)

    # Draw to follow button
    app.buttonToFollow.draw(canvas)

    

def startMode_mousePressed(app, event):
    # Go to competitive mode
    app.buttonToCompetitive.isPressed(event, app)
    if app.buttonToCompetitive.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        # play /images/buttonClicked.wav
        app.mode = 'competitiveMode'

    # Go to followMode
    app.buttonToFollow.isPressed(event, app)
    if app.buttonToFollow.pressed:
        time.sleep(0.1)
        app.mode = 'followMode' 

    

############# COMPETITIVE MODE #####################

def competitiveMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)
    drawPaceCounter(app, canvas)

    # # Title
    # canvas.create_text(app.width/2, app.height/10, text = 'competitive', font = 'Visby 50 bold', fill = 'white')
    

def competitiveMode_mousePressed(app, event):
    app.mode = 'competitiveMode'

    # Variables
    app.counterDisplayBounds = [app.width/3, app.height/3, 2*app.width/3, 2*app.height/3]

    # Bounds Increase Pace
    app.upPaceBounds = [1.6*(app.width/3 + app.width/10), app.height/3, 2*(app.width/3 + app.width/10), 1.4*app.height/3]

    # Bounds Decrease Pace
    app.downPaceBounds = [1.6*(app.width/3 + app.width/10), 1.6*app.height/3, 2*(app.width/3 + app.width/10), 2*app.height/3]

    
    # Pause

    # Skip

    # Go back

    # Increase / Decrease pace
    if clickedRegion(event, app.upPaceBounds):
        time.sleep(0.1) 
        app.pace += 1

        # Substitute all files with changed paced ones
        # The only tempo we keep is the original song tempo, because all changes in pace will be done relative to that one
        for song in app.songs:
            changeTempo(song[1], song[0], app.pace)

    if clickedRegion(event, app.downPaceBounds):
        time.sleep(0.1)
        if app.pace > 0:
            app.pace -= 1
        

    # Back button
    if app.backButton.pressed:
        time.sleep(0.1)
        app.mode = 'startMode'


def competitiveMode_keyPressed(app, event):
    # if any key is pressed, automatically highlight first song, up and down arrows will highlight next song, etc. Set boundaries for highest and lowest songs. If d is clicked "and" one of the rectangles is highlighted, i.e. slightly different color from black, then remove that song from app.songs    
    pass

        
        

############# FOLLOW MODE #####################


def followMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)

    # # Title
    # canvas.create_text(app.width/2, app.height/10, text = 'followMode', font = 'Visby 42 bold italic', fill = 'white')

    
def followMode_mousePressed(app, canvas):
     if clickedRegion(event, app.backBounds):
            time.sleep(0.1)
            app.mode = 'startMode'

        


       





########## VIEW ##################
def drawBackground(app, canvas, fill):
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, app.height - app.margin, fill = fill, outline = 'black', width = 25)



def drawPaceCounter(app, canvas):
    # Draw Counter
    canvas.create_rectangle(app.counterDisplayBounds[0], app.counterDisplayBounds[1], app.counterDisplayBounds[2], app.counterDisplayBounds[3])

    # Draw text 1
    canvas.create_text((app.counterDisplayBounds[0] + app.counterDisplayBounds[2])/2, (app.counterDisplayBounds[1]+app.counterDisplayBounds[3])/2,  text = str(app.pace), font = 'Visby 80 bold', fill = 'white')

    # Draw 'Pace' text
    canvas.create_text((app.counterDisplayBounds[0] + app.counterDisplayBounds[2])/2, app.counterDisplayBounds[1] - (app.height/20),  text = 'PACE', font = 'Visby 40 bold', fill = 'white')

    # Draw up button
    canvas.create_rectangle(app.upPaceBounds[0], app.upPaceBounds[1], app.upPaceBounds[2], app.upPaceBounds[3])
    
    # Draw down button
    canvas.create_rectangle(app.downPaceBounds[0], app.downPaceBounds[1], app.downPaceBounds[2], app.downPaceBounds[3])

    

########## MAIN APP ################
def appStarted(app):
    app.margin = 0
    app.mode = 'startMode'

    # Code that should be here: app.songs = getSongs()
    # Temporary code:
    app.songs = []
    app.pace = 0

    
    # CREATING ALL THE BUTTONS WE NEED
      # Button to competitive
    app.buttonToCompetitive = Button('competitive', 1, app, 'white', 'orange')
    app.buttonToCompetitive.setSize(app.width/8, app.height/3.5, 7*app.width/8, 1.5*app.height/3.5)

      # Button to follow
    app.buttonToFollow = Button('follow', 1, app, 'white', 'green')
    app.buttonToFollow.setSize(app.width/8, app.height/3.5 + 1.2*app.height/5, 7*app.width/8, 1.5*app.height/3.5  + 1.2*app.height/5)
    
      # Button to back
    app.backButton = Button('BACK', 0.4, app, 'white', 'black')
    app.backButton.setSize(0.7*app.width, 0.9*app.height, 0.9*app.width, 0.95*app.height)


runApp(width = 400, height = 600)
