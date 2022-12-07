from cmu_112_graphics import *
from tkinter import *
from backend import *
from random import randint, shuffle
from PIL import Image, ImageTk, ImageSequence
from objects import *
import time


        
        
        
# Citation: using idea of "modes" presented in the course notes
######################### START MODE ###########################
def startMode_redrawAll(app, canvas):

    drawBackground(app, canvas, 'black')
    # Title
    canvas.create_text(app.width/2, app.height/8,
                       text = 'rhythm',
                       font = ("Comic Sans MS", 130, "bold"),
                       fill = 'lightblue')


    # Draw competitive button background
    drawRoundedRectangle(1.5*app.width/8 + 15, app.height/1.3 + 10,
                         3.6*app.width/8 + 15, 1.2*app.height/1.3 + 10,
                         'lightblue', 10, canvas)

    
    # Draw to competitive button
    app.buttonToCompetitive.draw(canvas)


    # Draw to follow button background
    drawRoundedRectangle(4.5*app.width/8 + 15, app.height/1.3 + 10,
                         6.5*app.width/8 + 15, 1.2*app.height/1.3 + 10,
                         'lightblue', 10, canvas)
    
    # Draw to follow button
    app.buttonToFollow.draw(canvas)


    # Draw NCS gif
    photoImage = app.spritePhotoImages[app.spriteCounter]
    # photoImage = app.scaleImage(photoImage, 0.5)
    canvas.create_image(app.width/2, 1.015*app.height/2, image=photoImage)
    
    

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

        # reset values
        app.scoreCounter.value = 0
        app.mode = 'intermediateFollowMode'


        

def startMode_timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

########################################################################


        

############################ COMPETITIVE MODE #####################

def competitiveMode_redrawAll(app, canvas):
    # Colors for background: very cool rgbString(0, 0, 100), rgbString(app.r,app.g,app.b)
    drawBackground(app, canvas, rgbString(app.r,app.g,app.b))
    app.road.draw(app, canvas)

    # Draw sky
    canvas.create_image(app.imageX, app.imageY, image=ImageTk.PhotoImage(app.skyImage))



    # Draw all buildings
    app.leftBuildings.draw(app, canvas)
    app.rightBuildings.draw(app, canvas)


    # Draw coin
    app.currentCoin.draw(app, canvas)
    
    # Draw appropiate arms
    app.currentRightArm.draw(app, canvas)
    app.currentLeftArm.draw(app, canvas)
    
    # Draw buttons and counters
    app.backButton.draw(canvas)
    app.paceCounter.draw(canvas)
    app.distanceCounter.draw(canvas)
    app.timeCounter.draw(canvas)
    app.scoreCounter.draw(canvas)


    # On / Off track messages
    # Only draw every 10 seconds with app.timeRunning % 10 == 0
    # try: print(app.timeRunning)e
    # except: pass

    if app.showingMessage: drawUserMessage(app, canvas)
    
              
    
def competitiveMode_mousePressed(app, event):
    print(event.x, event.y)
    
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'
        app.timerDelay = 20


        

def competitiveMode_keyPressed(app, event):
    if event.key == 'Space':            

        
        # Move surroinding objects faster if running faster
        # Move buildings: we simulate distance of further objects by moving them slower than the closer ones
        for building in app.leftBuildings.buildings:
            if building.y0 < app.height/2: building.move(app, 1)
            else: building.move(app, 1)

        for building in app.rightBuildings.buildings:
            if building.y0 < app.height/2: building.move(app, 1)
            else: building.move(app, 1)

            
                
        # HEAD BOBBING DOWN
        # Road perspective
        app.road.bottomLeftX -= 2
        app.road.bottomRightX += 2

        # Background image perspective
        app.imageY += 1




    # Movement of player's arms
    if event.key == 'Left':
        if app.leftArmDown.xi[2] > (app.road.bottomLeftX + 200) and app.leftArmUp.xi[2] > (app.road.bottomLeftX + 200):
            # Only move if don't go out frame
            for i in range(len(app.rightArmUp.xi)):
                app.rightArmUp.xi[i] -= 25

            for i in range(len(app.leftArmUp.xi)):
                app.leftArmUp.xi[i] -= 25
            
            for i in range(len(app.rightArmDown.xi)):
                app.rightArmDown.xi[i] -= 25
                
            for i in range(len(app.leftArmDown.xi)):
                app.leftArmDown.xi[i] -= 25

                
                    
    elif event.key == 'Right':
        # Only move if don't go out frame
        if app.rightArmDown.xi[2] < (app.road.bottomRightX - 200) and app.rightArmUp.xi[2] < (app.road.bottomRightX - 200):
            for i in range(len(app.rightArmUp.xi)):
                app.rightArmUp.xi[i] += 25

            for i in range(len(app.leftArmUp.xi)):
                app.leftArmUp.xi[i] += 25
            
            for i in range(len(app.rightArmDown.xi)):
                app.rightArmDown.xi[i] += 25
                
            for i in range(len(app.leftArmDown.xi)):
                app.leftArmDown.xi[i] += 25
            
                    


def competitiveMode_keyReleased(app, event):
    if event.key == 'Space':
        # HEAD BOBBING UP
# When your heads goes up, you go faster, so buildings and dashes approach the user faster than they would usually. So we add more movement to them.

        # If already in process of moving, reset counter
        if app.spacePressed == True: app.counter = 0
        else: app.spacePressed = True

        
        # Road perspective
        app.road.bottomLeftX += 2
        app.road.bottomRightX -= 2

        # Background image perspective
        app.imageY -= 1

        
        # Buildings        
        for building in app.leftBuildings.buildings:
            if building.y0 < app.height/2: building.move(app, 4)
            else: building.move(app, 7)

        for building in app.rightBuildings.buildings:
            if building.y0 < app.height/2: building.move(app, 4)
            else: building.move(app, 7)



        # Switching arm up
        app.isRightArmUp = not app.isRightArmUp

        if app.isRightArmUp == True:
            app.currentRightArm = app.rightArmUp
            app.currentLeftArm = app.leftArmDown
        else:
            app.currentRightArm = app.rightArmDown
            app.currentLeftArm = app.leftArmUp
        

        # ADD STEP INTO DISTANCE RUN
        # Convert back to float
        app.distanceCounter.value = float(app.distanceCounter.value)
        
        # Increase distance by whatever calculation
        app.distanceCounter.value += app.strideMeters
        
        # Make sure only displays two decimals        
        app.distanceCounter.value = reduceDecimals(app.distanceCounter.value)
    
        
            
def competitiveMode_timerFired(app):
    print(app.shakalaka)
    print(app.timerDelay)
    app.shakalaka += 1


    
    if app.start == True:
        # Since timerFired is set at 100, but only want every second, we compensate by substracting 0.1s
        app.timeCounter.value -= 0.03
        app.timeCounter.value = float(reduceDecimals(app.timeCounter.value))

    # Gif
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

    # MAKE ALL MOVEMENTS SURROUNDINGS
    # Move buildings: we simulate distance of further objects by moving them slower than the closer ones
    for building in app.leftBuildings.buildings:
        if building.y0 < app.height/2: building.move(app, 1.4)
        else: building.move(app, 3)

    for building in app.rightBuildings.buildings:
        if building.y0 < app.height/2: building.move(app, 1.4)
        else: building.move(app, 3)


    # Move dashes on road:
    for dash in app.road.roadDashes:
        if dash.y0 < app.height/2.2: dash.move(app, 1)
        else: dash.move(app, 1.5)



    if app.spacePressed == True:
        if app.counter <= 10:
            app.counter += 1
            
            for dash in app.road.roadDashes:
                if dash.y0 < app.height/2.2: dash.move(app, 2)
                else: dash.move(app, 4)

        else:
            app.counter = 0
            app.spacePressed = False        
        

    # MOVE CURRENT COIN
    # app.currentCoin.move(app, app.coinDisplacement)
    app.currentCoin.move(app, 16)
    if ( app.currentCoin.inContact(app.leftArmUp) or
         app.currentCoin.inContact(app.rightArmUp) ):
        # increase score
        app.scoreCounter.value += 1
        # reset coins
        app.COINS.resetCoins(app)



    # SONGS
    # Play next song if music stops playing
    if not app.playlist[app.c].isPlaying():
        # change counter value (not commiting error of passing index)
        if app.c <= len(app.playlist)-1:
            app.c += 1
            app.playlist[app.c].start()

        else:
            app.c = 0
            app.playlist[app.c].start()



    # Determine if player is on track or off track
    if float(app.distanceCounter.value) >= float(onTrackDistance(app)):
        app.on_track = True    
    else: app.on_track = False
        

    # Check if runner made the objective
    checkRunnerFinished(app)


    # TESTING OUT MESSAGES
    try:
        if app.timeRunning % 10 == 0:
            app.showingMessage = True
            app.elapsed = time.time()

            if app.elapsed < 3: pass
            else:
                app.elapsed = 0
                app.showingMessage = False
                
            
    except: pass

########################################################################
        



################### INTERMEDIATE PAGE ################################

def intermediateMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')

    
    # Draw next button
    app.intermediateToCompetitive.draw(canvas)
    

    # Draw Title:
    canvas.create_text(app.width/2, app.height/10,
                       text = "Today's goals",
                       font = ("Comic Sans MS", 70, "bold"),
                       fill = 'lightgreen')

    canvas.create_text(app.width/2, 1.8*app.height/10,
                       text = "(Click on each category to type your info)",
                       font = ("Comic Sans MS", 30, "bold"),
                       fill = 'lightyellow')
    
    # Draw textBox for Goal Distance
    app.timeTextBox.draw(canvas)
    app.distanceTextBox.draw(canvas)
    app.heightTextBox.draw(canvas)




def intermediateMode_mousePressed(app, event):        
    # Go to competitive mode:
    app.intermediateToCompetitive.isPressed(event, app)

    if app.intermediateToCompetitive.pressed:
        transitionToCompetitive(app)

        
        
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
    if event.key != 'Enter' and hasattr(app, 'currentTextBox'): # making sure app has currentTextBox attribute

        # Only allow digits: making sure user can't delete full text box
        if ( ( event.key in {'0','1','2','3','4','5','6','7','8','9'} 
               or event.key == '.' )
             and len(app.currentTextBox.text) < 31 ):
            app.currentTextBox.text += event.key

        # Delete
        elif ( (event.key == 'Delete' or event.key == 'BackSpace')
            and app.currentTextBox.text[-1] != ' ' ): 
            app.currentTextBox.text = app.currentTextBox.text[:-1]


####################################################################
    




############## INTERMEDIATE FOLLOW MODE #########################

def intermediateFollowMode_redrawAll(app, canvas):
    # Background
    drawBackground(app, canvas, 'black')

    # TITLE

    # Title background
    drawRoundedRectangle(0.2*app.width + 20, 0.6*app.height + 20,
                         0.8*app.width + 20, 0.8*app.height + 20,
                         'yellow', 10, canvas)
    
    drawRoundedRectangle(0.3*app.width, 0.05*app.height,
                         0.7*app.width, 0.2*app.height,
                         'blue', 10, canvas)
    
    # Title text
    canvas.create_text(app.width/2, 0.117*app.height,
                       text = 'Adaptive',
                       font = ("Comic Sans MS", 75, "bold"),
                       fill = 'white')
    
    
    # Instructions
    canvas.create_text(app.width/2.5, 0.35*app.height,
                       text = '''
                       1) Begin running by clicking the space bar
                       2) Rhythm will calculate and display your current pace
                       3) Click 'Enter' when you have found a pace you are
                       comfortable with''',
                       font = ("Comic Sans MS", 30, "bold"),
                       fill = 'lightgreen')


    
    # Clicks per second
    drawRoundedRectangle(0.2*app.width + 20, 0.6*app.height + 20,
                         0.8*app.width + 20, 0.8*app.height + 20,
                         'yellow', 10, canvas)
    
    drawRoundedRectangle(0.2*app.width, 0.6*app.height,
                             0.8*app.width, 0.8*app.height,
                             'lightyellow', 10, canvas)


        
    try: text = f'Live pace: {app.bpm_Tempo}'
    except: text = f'Live pace: 0'
    
    canvas.create_text(app.width/2, 0.7*app.height,
                       text = text,
                       font = ("Comic Sans MS", 75, "bold"),
                       fill = 'green')



        

def intermediateFollowMode_keyPressed(app, event):
    # Register
    if event.key == 'Space': app.bpm_Tempo = estimateClicks()

    # Stop tracking and start running
    elif event.key == 'Enter' or event.key == 'Return':
        transitionToFollowMode(app)
    
       
###################################################







##### FOLLOW  MODE (alias functions in competitive mode) #######

followMode_redrawAll = competitiveMode_redrawAll

followMode_mousePressed = competitiveMode_mousePressed

followMode_keyPressed = competitiveMode_keyPressed

followMode_keyReleased = competitiveMode_keyReleased
        
followMode_timerFired = competitiveMode_timerFired    
            
###############################################################







################### CONGRATULATIONS MODE ###############

def congratulationsMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)

    
    # Draw Title:
    canvas.create_text(app.width/2, app.height/2,
                       text = "Congratulations!!! \n You achieved\n your goal!",
                       font = 'Visby 60 bold',
                       fill = 'lightgreen')




def congratulationsMode_mousePressed(app, event):        
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'
        app.timerDelay = 20


####################################################################







################### IMPROVEMENT MODE ###############

def improvementMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.backButton.draw(canvas)


    # Draw Title:
    canvas.create_text(app.width/2, app.height/2,
                       text = "You didn't make your goal! \n But don't give up! \n Keep working at it!",
                       font = 'Visby 60 bold',
                       fill = 'orange')



def improvementMode_mousePressed(app, event):        
    # If back button pressed:
    app.backButton.isPressed(event, app)
    if app.backButton.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'
        app.timerDelay = 20


####################################################################





################### INSTRUCTIONS MODE ###############

def instructionsMode_redrawAll(app, canvas):
    # Main
    drawBackground(app, canvas, 'black')
    app.instructionsToStart.draw(canvas)


    
    # Draw Title:
    canvas.create_text(app.width/2, 0.1*app.height,
                       text = 'Welcome to Rhythm!',
                       font = ("Comic Sans MS", 80, "bold"),
                       fill = 'lightgreen')



    # Draw instructions background
    drawRoundedRectangle(0.1*app.width + 30, 0.21*app.height + 10,
                         0.92*app.width + 10, 0.85*app.height + 10,
                         'darkblue', 10, canvas)

    drawRoundedRectangle(0.1*app.width +20, 0.21*app.height - 10,
                         0.92*app.width - 10, 0.85*app.height - 10,
                         'blue', 10, canvas)
    
    # Draw instructions
    canvas.create_text(app.width/2, app.height/2,
                       text = app.instructions,
                       font = ("Comic Sans MS", 30, "bold"),
                       fill = 'lightgreen')

    canvas.create_oval(app.TESTX + 10, app.height/2 + 10,
                       app.TESTX - 10, app.height/2 - 10,
                       fill = 'red')



def instructionsMode_mousePressed(app, event):        
    # If back button pressed:
    app.instructionsToStart.isPressed(event, app)
    if app.instructionsToStart.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'
        app.timerDelay = 20

        

def instructionsMode_keyReleased(app, event):
    if event.key == 'Space':
        # If already in process of moving, reset counter
        if app.spacePressed == True: app.counter = 0
        else: app.spacePressed = True


        
def instructionsMode_timerFired(app):
    app.TESTX += 0.05
    
    if app.spacePressed == True:
        if app.counter <= 10:
            app.counter += 1
            app.TESTX += 1
        else:
            app.counter = 0
            app.spacePressed = False
        


####################################################################





    

############################ MAIN APP ###############################
def appStarted(app):
    app.TESTX = app.width/4
    app.mode = 'instructionsMode'
    setupInstructions(app)
    app.showingMessage = False

    
    app.imageX = app.width/2
    # app.imageY = 0.01*app.height
    app.imageY = 0.2*app.height

    
    app.start = False
    app.isRightArmUp = False # boolean for movement of arms in 3D
    app.margin = 0
    app.colors = ['green', 'purple', 'pink', 'red',
                  'yellow', 'blue', 'orange']
    app.currentColor = app.colors[randint(0,len(app.colors)-1)]

    app.c = 0 # index of the song playlist 
    
    app.cx = app.width/2 # x of point 3D graphics point to
    app.cy = (app.height/4) # y of point 3D graphics point to

    app.lx = app.width/2 # second 3D point
    app.ly = (1.2*app.height/4)

    app.playlist = getOriginalSongs()

    # Loading gif
    app.spritePhotoImages = loadAnimatedGif('images/green_ncs.gif')
    app.spriteCounter = 0


    ######## EDITS TESTING COUNTER
    app.timerDelay = 0
    app.counter = 0
    app.spacePressed = False

    # Loading image of sky
    app.skyImage = app.loadImage('images/sky2 copy.png')
    app.skyImage = app.scaleImage(app.skyImage, 0.73) # rescale

    
    
    ########### CREATING ALL THE BUTTONS WE NEED #####################
      # Button to competitive
    app.buttonToCompetitive = Button('Set Goal', 0.85, app,
                                     'white', 'blue', 'blue')
    app.buttonToCompetitive.setSize(1.5*app.width/8, app.height/1.3,
                                    3.6*app.width/8, 1.2*app.height/1.3)

      # Button to follow
    app.buttonToFollow = Button('Adaptive', 0.4, app,
                                'white', 'blue', 'blue')
    app.buttonToFollow.setSize(4.5*app.width/8, app.height/1.3,
                               6.5*app.width/8, 1.2*app.height/1.3)
    
      # Button to back
    app.backButton = Button('BACK', 0.2, app, 'white', 'blue', 'blue')
    app.backButton.setSize(0.87*app.width, 0.90*app.height,
                           0.97*app.width, 0.96*app.height)
      # Button intermediate to competitive
    app.intermediateToCompetitive = Button('NEXT', 0.2, app, 'white', 'blue', 'blue')
    app.intermediateToCompetitive.setSize(0.87*app.width, 0.90*app.height,
                                          0.97*app.width, 0.96*app.height)

    # Button instructions to start
    app.instructionsToStart = Button('NEXT', 0.2, app, 'white', 'blue', 'blue')
    app.instructionsToStart.setSize(0.88*app.width, 0.91*app.height,
                                    0.98*app.width, 0.97*app.height)

      
    ##################################################################

    
    
    ########### CREATING ALL THE COUNTERS WE NEED #####################
      # Pace Counter
    app.paceCounter = Counter('Pace: ', 1, 'black', 'lightblue', app, 0.42, '')
    app.paceCounter.setSize((app.width/2) - 100, 0.5*app.height/20,
                            (app.width/2) + 100, 0.5*1.5*app.height/12)    

      # Distance Counter
    app.distanceCounter = Counter('Distance: ', 0, 'lightblue', rgbString(0, 0, 100), app, 0.34, 'm')
    app.distanceCounter.setSize(6.5*app.width/20, 1.4*app.height/18,
                                10*app.width/20, 2*app.height/18)    

      # Time Counter
    app.timeCounter = Counter('Time: ', 100, 'lightblue', rgbString(0, 0, 100), app, 0.23, 's')
    app.timeCounter.setSize(10.3*app.width/20, 1.4*app.height/18,
                            12.8*app.width/20, 2*app.height/18)

    # Score Counter
    app.scoreCounter = Counter('Score: ', 0, 'lightblue', rgbString(0, 0, 100), app, 0.27, '')
    app.scoreCounter.setSize(9*app.width/20, 2.2*app.height/18,
                            11*app.width/20, 2.8*app.height/18)
    
    ##################################################################


    ################### CREATING ALL THE TEXTBOXES ##################
    app.distanceTextBox = TextBox(app, "Distance goal (meters) : ", 0.45, 'blue', 'black')
    app.distanceTextBox.setSize(0.1*app.width, 0.28*app.height,
                                0.9*app.width, 0.38*app.height)

    
    app.timeTextBox = TextBox(app, "Time goal (minutes) : ", 0.45, 'blue', 'black')
    app.timeTextBox.setSize(0.1*app.width, 0.48*app.height,
                            0.9*app.width, 0.58*app.height)

    app.heightTextBox = TextBox(app, "Height (meters) : ", 0.5, 'blue', 'black')
    app.heightTextBox.setSize(0.1*app.width, 0.68*app.height,
                              0.9*app.width, 0.78*app.height)

    ################################################################



    # CREATING 3D GRAPHICS
    # Creating road
    app.road = Road(app, 'gray', 'yellow')
    app.road.setSize(-0.05*app.width, 1.2*app.height,
                     1.05*app.width, 1.2*app.height)

    # Creating building class
    app.leftBuildings = LeftBuildings(app)
    app.rightBuildings = RightBuildings(app)

    # Setting up color for floor of floor next to road
    # Citation: getpixel code obtained from 112 notes
    app.rgbForm = app.skyImage.convert('RGB')
    # app.r, app.g, app.b = app.rgbForm.getpixel((550, 580))
    app.r, app.g, app.b = app.rgbForm.getpixel((800, 300))


    # Create Arms
# Creating right Arm
    # ORIGINAL ARM
    app.rightArmUp = Arm(app,
                   700, 600,
                   790, 620,
                   850, app.height,                       
                   750, app.height,
                       
                   700, app.height,
                   670, 650)

    app.rightArmDown = Arm(app,
                   700, 700,
                   790, 720,
                   850, app.height,                       
                   750, app.height,
                       
                   700, app.height,
                   670, 750)

    # creating symmetry with right arm
    app.leftArmUp = Arm(app,
                   (app.width/2)-(700-(app.width/2)), 600,
                   (app.width/2)-(790-(app.width/2)), 620,
                   (app.width/2)-(850-(app.width/2)), app.height,                       
                   (app.width/2)-(750-(app.width/2)), app.height,
                       
                   (app.width/2)-(700-(app.width/2)), app.height,
                   (app.width/2)-(670-(app.width/2)), 650)


    app.leftArmDown = Arm(app,
                   (app.width/2)-(700-(app.width/2)), 700,
                   (app.width/2)-(790-(app.width/2)), 720,
                   (app.width/2)-(850-(app.width/2)), app.height,                       
                   (app.width/2)-(750-(app.width/2)), app.height,
                       
                   (app.width/2)-(700-(app.width/2)), app.height,
                   (app.width/2)-(670-(app.width/2)), 750)

    # By default, we set right arm to be up and left arm down
    app.currentRightArm = app.rightArmUp
    app.currentLeftArm = app.leftArmDown
    

    # # Creating coins
    app.COINS = AllCoins(app)
    app.coinIndex = 0
    app.currentCoin = app.COINS.coins[app.coinIndex]

                
    
runApp(width = 1160, height = 800)
