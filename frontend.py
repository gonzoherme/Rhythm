from cmu_112_graphics import *
from tkinter import *
import time
from backend import *
# from opencv import *
from random import randint
import time
from PIL import Image, ImageTk, ImageSequence
from objects import *
from random import randint



        
# Citation: using idea of "modes" presented in the course notes
######################### START MODE ###########################
def startMode_redrawAll(app, canvas):
    drawBackground(app, canvas, 'black')
    # Title
    canvas.create_text(app.width/2, app.height/10, text = 'rhythm', font = 'Visby 100 bold', fill = 'lightgreen')
    
    # Draw to competitive button
    app.buttonToCompetitive.draw(canvas)

    # Draw to follow button
    app.buttonToFollow.draw(canvas)

    # Draw NCS gif
    photoImage = app.spritePhotoImages[app.spriteCounter]
    canvas.create_image(200, 200, image=photoImage)


    

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
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'followMode'


def startMode_timerFired(app): # NOT WORKING!
    # app.timeCounter.value -= 1
    # print(app.timeCounter.value)
    # print('x')
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)
    print(len(app.spritePhotoImages))

########################################################################


        

################################# COMPETITIVE MODE #####################


def competitiveMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)
    app.paceCounter.draw(canvas)
    app.distanceCounter.draw(canvas)
    app.timeCounter.draw(canvas)
    


    
def competitiveMode_mousePressed(app, event):
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'    

    
    # Pause

    # Skip

    # Go back

    # Increase / Decrease pace

        # Substitute all files with changed paced ones
        # The only tempo we keep is the original song tempo, because all changes in pace will be done relative to that one
        # for song in app.playlist:
        #     changeTempo(song[1], song[0], app.pace)

        

def competitiveMode_keyPressed(app, event):
    # if any key is pressed, automatically highlight first song, up and down arrows will highlight next song, etc. Set boundaries for highest and lowest songs. If d is clicked "and" one of the rectangles is highlighted, i.e. slightly different color from black, then remove that song from app.playlist
    if event.key == 'Space':
        print('Space')

    # Press enter to start playing songs
    if event.key == 'Enter':
        # Play a random song
        index = randint(0, len(app.playlist)-1)
        app.playlist[index].start()
        

    # temporary code that will be replaced with opencv
    elif event.key == 'Up':
        if app.paceCounter.value < 20:
            app.paceCounter.value += 1

    elif event.key == 'Down':
        if app.paceCounter.value > 0:
            app.paceCounter.value -= 1

    
########################################################################
        
        




################################ FOLLOW MODE #########################


def followMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)

    # # Title
    # canvas.create_text(app.width/2, app.height/10, text = 'followMode', font = 'Visby 42 bold italic', fill = 'white')

    
def followMode_mousePressed(app, event):
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode' 



       

########################################################################






########## VIEW ##################
def drawBackground(app, canvas, fill):
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, app.height - app.margin, fill = fill, outline = 'black', width = 25)
##################################






    

    

#################################### MAIN APP #####################################
def appStarted(app):
    app.margin = 0
    app.timerDelay = 1
    app.mode = 'startMode'

    app.playlist = getSongs() #[]

    
    print(app.playlist)

    
    ########### CREATING ALL THE BUTTONS WE NEED #####################
      # Button to competitive
    app.buttonToCompetitive = Button('competitive', 1, app, 'white', 'blue')
    app.buttonToCompetitive.setSize(app.width/8, app.height/3.5, 7*app.width/8, 1.5*app.height/3.5)

      # Button to follow
    app.buttonToFollow = Button('follow', 1, app, 'white', 'blue')
    app.buttonToFollow.setSize(app.width/8, app.height/3.5 + 1.2*app.height/5, 7*app.width/8, 1.5*app.height/3.5  + 1.2*app.height/5)
    
      # Button to back
    app.backButton = Button('BACK', 0.4, app, 'white', 'black')
    app.backButton.setSize(0.8*app.width, 0.9*app.height, 0.9*app.width, 0.95*app.height)

    ##################################################################


    
    
    ########### CREATING ALL THE COUNTERS WE NEED #####################
      # Pace Counter
    app.paceCounter = Counter('Pace: ', 1/2, 'lightgreen', 'black', app, 0.68)
    app.paceCounter.setSize(app.width/8, app.height/20, 7*app.width/8, 1.5*app.height/12)    

      # Distance Counter
    app.distanceCounter = Counter('Distance: ', 100, 'lightblue', 'black', app, 1)
    app.distanceCounter.setSize(app.width/10, 1.4*app.height/18, 2.1*app.width/10, 2*app.height/18)    

      # Time Counter
    app.timeCounter = Counter('Time: ', 100, 'red', 'black', app, 1)
    app.timeCounter.setSize(app.width/10, app.height/18, 2*app.width/10, 1.5*app.height/18)        
    
    ##################################################################



    # Changing pace to adequate pace
    for song in app.playlist:
        song.changeTempo(app.paceCounter.value)

    
    app.spritePhotoImages = loadAnimatedGif('images/green_ncs.gif')
    app.spriteCounter = 0
    


    

####################################################################################################
    
runApp(width = 700, height = 800)
