from cmu_112_graphics import *
from tkinter import *
from backend import *
# from opencv import *
from random import randint, shuffle
from PIL import Image, ImageTk, ImageSequence
from objects import *
from random import randint


        
        
        
# Citation: using idea of "modes" presented in the course notes
######################### START MODE ###########################
def startMode_redrawAll(app, canvas):

    drawBackground(app, canvas, 'black')
    # Title
    canvas.create_text(app.width/2, app.height/10,
                       text = 'rhythm', font = 'Visby 100 bold', fill = 'lightblue')


    
    # Draw to competitive button
    app.buttonToCompetitive.draw(canvas)

    # Draw to follow button
    app.buttonToFollow.draw(canvas)


    # Draw NCS gif
    photoImage = app.spritePhotoImages[app.spriteCounter]
    # photoImage = app.scaleImage(photoImage, 0.5)
    canvas.create_image(app.width/2, 0.9 *app.height/2, image=photoImage)
    
    

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


        

def startMode_timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)
    # print(len(app.spritePhotoImages))

########################################################################


        

################################# COMPETITIVE MODE #####################


def competitiveMode_redrawAll(app, canvas):
    drawBackground(app, canvas, 'black')

    app.road.draw(app, canvas)

    # Draw sky
    canvas.create_image(app.width/2, -0.1*app.height, image=ImageTk.PhotoImage(app.skyImage))

    # Draw gif
    # photoImage = app.spritePhotoImages[app.spriteCounter]
    # # photoImage = app.scaleImage(photoImage, 0.5)
    # canvas.create_image(3*app.width/4, app.height/8, image=photoImage)


    # Draw buttons and buttons
    app.backButton.draw(canvas)
    app.paceCounter.draw(canvas)
    app.distanceCounter.draw(canvas)
    app.timeCounter.draw(canvas)

    # Check if runner done
    if app.timeCounter.value == 0 and app.distanceCounter.value < app.distanceMeters:
        # did not make the objective
        app.mode = 'improvementMode'



    app.leftBuildings.draw(app, canvas)
    app.rightBuildings.draw(app, canvas)


    
def competitiveMode_mousePressed(app, event):
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'
        app.timerDelay = 20

    # All of this with opencv    
    # Pause, skip, back, increase / decrease pace

        

def competitiveMode_keyPressed(app, event):
    if event.key == 'Space':
        #convert back to float
        app.distanceCounter.value = float(app.distanceCounter.value)
        # increase distance by whatever calculation
        app.distanceCounter.value += app.strideMeters
        # make sure only displays two decimals        
        app.distanceCounter.value = reduceDecimals(app.distanceCounter.value)

        
        # check if full distance reached
        if float(app.distanceCounter.value) >= app.distanceMeters:
            # Congrats!
            app.mode = 'congratulationsMode'
            resetAll(app)

            
        

    # Press enter to start playing songs
    if event.key == 'Enter' or event.key == 'Return':
        # We start to play the songs, as well as start the countdown
        app.start = True

        # Play our playlist
        # Shuffle the playlist
        shuffle(app.playlist)
        c = 0
        app.playlist[0].start()
        #play next song if P
        
        

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
    if app.start == True:
        app.timeCounter.value -= 1

    # Gif
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

    # MAKE ALL MOVEMENTS SURROUNDINGS
    # Move buildings: we simulate distance of further objects by moving them slower than the closer ones
    for building in app.leftBuildings.buildings:
        if building.y0 < app.height/2:
            building.move(app, 2)
        else:
            building.move(app, 4)

    for building in app.rightBuildings.buildings:
        if building.y0 < app.height/2:
            building.move(app, 2)
        else:
            building.move(app, 4)


    # Move dashes on road:
    for dash in app.road.roadDashes:
        if dash.y0 < app.height/2:
            dash.move(app, 5)
        else:
            dash.move(app, 10)

    
            
########################################################################
        



################### INTERMEDIATE PAGE ################################



def intermediateMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    # Draw next button
    app.intermediateToCompetitive.draw(canvas)
    

    # Draw Title:
    canvas.create_text(app.width/2, app.height/10, text = "Today's goals: ",
                       font = 'Visby 60 bold', fill = 'lightgreen')
    
    # Draw textBox for Goal Distance
    app.timeTextBox.draw(canvas)
    app.distanceTextBox.draw(canvas)
    app.heightTextBox.draw(canvas)





def intermediateMode_mousePressed(app, event):        
    # Go to competitive mode:
    app.intermediateToCompetitive.isPressed(event, app)
    if app.intermediateToCompetitive.pressed:
        # UNCOMMENT FOR FULL FUNCTIONALITY
        # Reset distance from previous session
        if app.distanceCounter.value != 0:
            app.distanceCounter.value = 0
        
        # Setup all the required data
        setRequiredParameters(app)
        
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'competitiveMode'
        app.timerDelay = 100

        # Changing songs to set pace
        for song in app.playlist:
            song.changeTempo(app.stepsPerMinute)

        app.playlist = getAlteredSongs()

        
        
    # Input text if any of the text boxes are clicked
    app.distanceTextBox.isPressed(event, app)
    if app.distanceTextBox.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.currentTextBox = app.distanceTextBox # creating an alias on purpose
        

    app.timeTextBox.isPressed(event, app)
    if app.timeTextBox.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.currentTextBox = app.timeTextBox # creating an alias on purpose
        
    app.heightTextBox.isPressed(event, app)
    if app.heightTextBox.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.currentTextBox = app.heightTextBox # creating an alias on purpose\


        
def intermediateMode_keyPressed(app, event):
    if event.key != 'Enter' and hasattr(app, 'currentTextBox'): #making sure app has currentTextBox attribute
        if event.key == 'Space':
            app.currentTextBox.text += ' '
        elif ((event.key == 'Delete' or event.key == 'BackSpace')
              and app.currentTextBox.text[-1] != ':') : # making sure user can't delete full text box
            app.currentTextBox.text = app.currentTextBox.text[:-1]
        else:
            app.currentTextBox.text += event.key



####################################################################


    


################################ FOLLOW MODE #########################

def followMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.intermediateToCompetitive.draw(canvas)

    # Title
    canvas.create_text(app.width/2, app.height/10,
                       text = "Start running \n we'll adjust your songs \n to your pace",
                       font = 'Visby 42 bold italic', fill = 'white')

    
def followMode_mousePressed(app, event):
    # If back button pressed:
    app.intermediateToCompetitive.isPressed(event, app)
    if app.intermediateToCompetitive.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'competitiveMode' 

        # Reset distance from previous session
        if app.distanceCounter.value != 0:
            app.distanceCounter.value = 0
        
        # Setup all the required data
        record 
        
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'competitiveMode'
        app.timerDelay = 100

        # Changing songs to set pace
        for song in app.playlist:
            song.changeTempo(app.stepsPerMinute)

        app.playlist = getAlteredSongs()

       

########################################################################







######################### CONGRATULATIONS MODE ########################

def congratulationsMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)

    # Draw Title:
    canvas.create_text(app.width/2, app.height/2,
                       text = "Congratulations!!! \n You achieved\n your goal!",
                       font = 'Visby 60 bold', fill = 'lightgreen')





def congratulationsMode_mousePressed(app, event):        
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode' 


#######################################################################

    

    

#################################### MAIN APP #####################################
def appStarted(app):
    app.start = False
    app.margin = 0

    app.cx = app.width/2 # x of point 3D graphics point to
    app.cy = (app.height/4) # y of point 3D graphics point to

    app.lx = app.width/2 # second 3D point
    app.ly = (1.2*app.height/4)
    
    app.mode = 'competitiveMode'

    app.playlist = getOriginalSongs()

    # Loading gif
    app.spritePhotoImages = loadAnimatedGif('images/green_ncs.gif')
    app.spriteCounter = 0
    app.timerDelay = 20


    # Loading image of sky
    app.skyImage = app.loadImage('images/sky2.png')
    app.skyImage = app.scaleImage(app.skyImage, 1) # rescale

    
    
    ########### CREATING ALL THE BUTTONS WE NEED #####################
      # Button to competitive
    app.buttonToCompetitive = Button('Set Goal', 0.7, app, 'white', 'blue')
    app.buttonToCompetitive.setSize(1.5*app.width/8, app.height/1.3,
                                    3.6*app.width/8, 1.2*app.height/1.3)

      # Button to follow
    app.buttonToFollow = Button('Adaptive', 0.32, app, 'white', 'blue')
    app.buttonToFollow.setSize(4.5*app.width/8, app.height/1.3,
                               6.5*app.width/8, 1.2*app.height/1.3)
    
      # Button to back
    app.backButton = Button('BACK', 0.2, app, 'white', 'black')
    app.backButton.setSize(0.88*app.width, 0.93*app.height,
                           0.96*app.width, 0.96*app.height)

      # Button intermediate to competitive
    app.intermediateToCompetitive = Button('NEXT', 0.2, app, 'white', 'black')
    app.intermediateToCompetitive.setSize(0.88*app.width, 0.93*app.height,
                                          0.96*app.width, 0.96*app.height)

      
    ##################################################################

    
    
    ########### CREATING ALL THE COUNTERS WE NEED #####################
      # Pace Counter
    app.paceCounter = Counter('Pace: ', 1, 'black', 'lightblue', app, 0.5, '')
    app.paceCounter.setSize((app.width/2) - 100, 0.5*app.height/20,
                            (app.width/2) + 100, 0.5*1.5*app.height/12)    

      # Distance Counter
    app.distanceCounter = Counter('Distance: ', 0, 'lightblue', rgbString(0, 0, 100), app, 0.3, 'm')
    app.distanceCounter.setSize(8*app.width/20, 1.4*app.height/18,
                                10*app.width/20, 2*app.height/18)    

      # Time Counter
    app.timeCounter = Counter('Time: ', 100, 'lightblue', rgbString(0, 0, 100), app, 0.25, 's')
    app.timeCounter.setSize(10.3*app.width/20, 1.4*app.height/18,
                            12.1*app.width/20, 2*app.height/18)       
    
    ##################################################################


    ################### CREATING ALL THE TEXTBOXES ##################
    app.distanceTextBox = TextBox(app, "Distance goal: ", 0.7, 'lightblue', 'black')
    app.distanceTextBox.setSize(1.5*app.width/20, app.height/3.5,
                                1.5*10*app.width/20, 1.5*app.height/3.5)

    
    app.timeTextBox = TextBox(app, "Time goal: ", 0.7, 'lightyellow', 'black')
    app.timeTextBox.setSize(1.5*app.width/20, 1.5*app.height/3.5,
                            1.5*10*app.width/20, 1.4*1.5*app.height/3.5)

    app.heightTextBox = TextBox(app, "Height: ", 0.7, 'lightgreen', 'black')
    app.heightTextBox.setSize(1.5*app.width/20, 2.2*app.height/3.5,
                              1.5*10*app.width/20, 1.6*1.5*app.height/3.5)    
    ################################################################



    # CREATING 3D GRAPHICS
    # Creating road
    app.road = Road(app, 'gray', 'yellow')
    app.road.setSize(-0.05*app.width, 1.2*app.height, 1.05*app.width, 1.2*app.height)

    # Creating building class
    app.leftBuildings = LeftBuildings(app)
    app.rightBuildings = RightBuildings(app)

    
    
runApp(width = 1160, height = 800)
