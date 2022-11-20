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



def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e:
            return spritePhotoImages

        
        
        
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
        app.mode = 'intermediateMode'
        app.timerDelay = 1000

    # Go to followMode
    app.buttonToFollow.isPressed(event, app)
    if app.buttonToFollow.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'followMode'


        

def startMode_timerFired(app): # NOT WORKING!
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)
    # print(len(app.spritePhotoImages))

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
        app.timerDelay = 1

    
    # Pause
    # All of this with opencv
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
        # increase distance by whatever calculation
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

            # change tempo in all songs (not implemented yet)
            # for song in app.playlist:
            #     song.changeTempo(app.paceCounter.value)

    elif event.key == 'Down':
        if app.paceCounter.value > 0:
            app.paceCounter.value -= 1

            # change tempo in all songs (not implemented yet)
            # for song in app.playlist:
            #     song.changeTempo(app.paceCounter.value)


            
def competitiveMode_timerFired(app):
    app.timeCounter.value -= 1

            
########################################################################
        



################### INTERMEDIATE PAGE ################################



def intermediateMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    # Draw next button
    app.intermediateToCompetitive.draw(canvas)
    

    # Draw Title:
    canvas.create_text(app.width/2, app.height/10, text = "Today's goals: ", font = 'Visby 60 bold', fill = 'lightgreen')
    
    # Draw textBox for Goal Distance
    # app.distanceTextBox.draw(canvas)
    # app.heightTextBox.draw(canvas)




    


def intermediateMode_mousePressed(app, event):        
    # Go to competitive mode:
    app.intermediateToCompetitive.isPressed(event, app)
    if app.intermediateToCompetitive.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'competitiveMode'
        app.timerDelay = 1000

        # Setup adequate pace
        app.pace = calculatePace(app)


        
    # Input text if text box clicked
    app.distanceTextBox.isPressed(event, app)
    if app.distanceTextBox.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.currentTextBox = app.distanceTextBox # creating an alias on purpose
        


        
        
def intermediateMode_keyPressed(app, event):
    if event.key != 'Enter' and hasattr(app, 'currentTextBox'): #making sure app has currentTextBox attribute
        if event.key == 'Space':
            app.currentTextBox.text += ' '
        elif event.key == 'Delete' and app.currentTextBox.text[-1] != ':' : # making sure user can't delete full text box
            app.currentTextBox.text = app.currentTextBox.text[:-1]
        else:
            app.currentTextBox.text += event.key



####################################################################


    


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
    app.mode = 'startMode'

    app.playlist = getOriginalSongs()
    print(app.playlist)

    # Loading gif
    app.spritePhotoImages = loadAnimatedGif('images/green_ncs.gif')
    app.spriteCounter = 0
    app.timerDelay = 40

    
    # print(app.playlist)

    
    ########### CREATING ALL THE BUTTONS WE NEED #####################
      # Button to competitive
    app.buttonToCompetitive = Button('competitive', 1, app, 'white', 'blue')
    app.buttonToCompetitive.setSize(app.width/8, app.height/3.5, 7*app.width/8, 1.5*app.height/3.5)

      # Button to follow
    app.buttonToFollow = Button('follow', 1, app, 'white', 'blue')
    app.buttonToFollow.setSize(app.width/8, app.height/3.5 + 1.2*app.height/5, 7*app.width/8, 1.5*app.height/3.5  + 1.2*app.height/5)
    
      # Button to back
    app.backButton = Button('BACK', 0.3, app, 'white', 'black')
    app.backButton.setSize(0.8*app.width, 0.9*app.height, 0.9*app.width, 0.95*app.height)

      # Button intermediate to competitive
    app.intermediateToCompetitive = Button('NEXT', 0.3, app, 'white', 'black')
    app.intermediateToCompetitive.setSize(0.8*app.width, 0.9*app.height, 0.9*app.width, 0.95*app.height)

      
    ##################################################################


    
    
    ########### CREATING ALL THE COUNTERS WE NEED #####################
      # Pace Counter
    app.paceCounter = Counter('Pace: ', 1, 'lightgreen', 'black', app, 0.68, '')
    app.paceCounter.setSize(app.width/8, app.height/20, 7*app.width/8, 1.5*app.height/12)    

      # Distance Counter
    app.distanceCounter = Counter('Distance: ', 0, 'lightblue', 'black', app, 1, 'm')
    app.distanceCounter.setSize(app.width/10, 1.4*app.height/18, 2.1*app.width/10, 2*app.height/18)    

      # Time Counter
    app.timeCounter = Counter('Time: ', 100, 'lightyellow', 'black', app, 1, 's')
    app.timeCounter.setSize(app.width/10, app.height/18, 2*app.width/10, 1.5*app.height/18)        
    
    ##################################################################


    ################### CREATING ALL THE TEXTBOXES ##################
    app.distanceTextBox = TextBox(app, "Distance goal: ", 1, 'lightblue', 'black')
    app.distanceTextBox.setSize(app.width/20, app.height/3.5, 10*app.width/20, 1.5*app.height/3.5)

    
    app.timeTextBox = TextBox(app, "Time goal: ", 1, 'lightyellow', 'black')
    app.timeTextBox.setSize(app.width/20, app.height/3.5, 10*app.width/20, 1.5*app.height/3.5)

    app.timeTextBox = TextBox(app, "Height: ", 1, 'lightyellow', 'black')
    app.timeTextBox.setSize(app.width/20, app.height/3.5, 10*app.width/20, 1.5*app.height/3.5)    
    ################################################################

    


    # Changing pace to adequate pace
    for song in app.playlist:
        song.changeTempo(app.paceCounter.value)
    # Setting all songs to initial altered tempo
    app.playlist = getAlteredSongs()



    


    

####################################################################################################
    
runApp(width = 700, height = 800)
