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
    canvas.create_text(app.width/2, app.height/10,
                       text = 'rhythm', font = 'Visby 100 bold',
                       fill = 'lightblue')


    
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
    # try: print(app.timeRunning)
    # except: pass

    if app.showingMessage: drawUserMessage(app, canvas)
    

             
    
    
    
def competitiveMode_mousePressed(app, event):
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


        # Dashes
        for dash in app.road.roadDashes:
            # movement
            if dash.y0 < app.height/2: dash.move(app, 5)
            else: dash.move(app, 10)
                
                
        # HEAD BOBBING DOWN
        # Road perspective
        app.road.bottomLeftX -= 3.8
        app.road.bottomRightX += 3.8

        # Background image perspective
        app.imageY += 2



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

        # if app.isRightArmUp == True:
        #     app.currentRightArm = app.rightArmUp
        #     app.currentLeftArm = app.leftArmDown
        # else:
        #     app.currentRightArm = app.rightArmDown
        #     app.currentLeftArm = app.leftArmUp
            
                
                    
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

            
        # if app.isRightArmUp == True:
        #     app.currentRightArm = app.rightArmUp
        #     app.currentLeftArm = app.leftArmDown
        # else:
        #     app.currentRightArm = app.rightArmDown
        #     app.currentLeftArm = app.leftArmUp  
                    



    

def competitiveMode_keyReleased(app, event):
    if event.key == 'Space':
        # HEAD BOBBING UP
# When your heads goes up, you go faster, so buildings and dashes approach the user faster than they would usually. So we add more movement to them.

        # Road perspective
        app.road.bottomLeftX += 3.8
        app.road.bottomRightX -= 3.8

        # Background image perspective
        app.imageY -= 2        

        
        # Buildings        
        for building in app.leftBuildings.buildings:
            if building.y0 < app.height/2: building.move(app, 4)
            else: building.move(app, 7)

        for building in app.rightBuildings.buildings:
            if building.y0 < app.height/2: building.move(app, 4)
            else: building.move(app, 7)


        # Dashes
        for dash in app.road.roadDashes:
            # # Make narrower
            # dash.x0 -= 5
            # dash.x1 -= 5
            # dash.x3 += 5
            # dash.x2 += 5
            
            
            # Move faster
            if dash.y0 < app.height/2: dash.move(app, 20)
            else: dash.move(app, 30)


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
    if app.start == True:
        # Since timerFired is set at 100, but only want every second, we compensate by substracting 0.1s
        app.timeCounter.value -= 0.1
        app.timeCounter.value = float(reduceDecimals(app.timeCounter.value))

    # Gif
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

    # MAKE ALL MOVEMENTS SURROUNDINGS
    # Move buildings: we simulate distance of further objects by moving them slower than the closer ones
    for building in app.leftBuildings.buildings:
        if building.y0 < app.height/2: building.move(app, 2)
        else: building.move(app, 4)

    for building in app.rightBuildings.buildings:
        if building.y0 < app.height/2: building.move(app, 2)
        else: building.move(app, 4)


    # Move dashes on road:
    for dash in app.road.roadDashes:
        if dash.y0 < app.height/2: dash.move(app, 3)
        else: dash.move(app, 8)

    # Move current coin
    if app.currentCoin.y0 < app.height/2:
        app.currentCoin.move(app, 6)

    else:
        # when in lower half
        app.currentCoin.move(app, 10)
        # check if coin in contact with arms
        if ( app.currentCoin.inContact(app.leftArmUp) or
            app.currentCoin.inContact(app.rightArmUp) ):
            # display green screen
            print('Touching detecting')
            app.scoreCounter.value += 1
            #reset
            app.COINS.coins[0].__init__(app, 530, 300, 50)
            app.COINS.coins[1].__init__(app, 630, 300, 50)
            app.currentCoin = app.COINS.coins[randint(0, len(app.COINS.coins) - 1)]


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
            

            
            print('Getting here')
            
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
                       font = 'Visby 60 bold',
                       fill = 'lightgreen')

    canvas.create_text(app.width/2, 1.8*app.height/10,
                       text = "(Click on each category to type your info)",
                       font = 'Visby 30 bold', fill = 'lightyellow')
    
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
    if event.key != 'Enter' and hasattr(app, 'currentTextBox'): #making sure app has currentTextBox attribute

        # Add space
        if event.key == 'Space':
            app.currentTextBox.text += ' '
    
        # Delete
        elif ((event.key == 'Delete' or event.key == 'BackSpace')
              and app.currentTextBox.text[-1] != ':') : # making sure user can't delete full text box
            app.currentTextBox.text = app.currentTextBox.text[:-1]

        # Checking for 'Enter' or 'Return'
        elif event.key == 'Enter' or event.key == 'Return': pass

        # Add character to text
        else: app.currentTextBox.text += event.key


####################################################################
    


############## INTERMEDIATE FOLLOW MODE #########################


def intermediateFollowMode_redrawAll(app, canvas):
    # Background
    drawBackground(app, canvas, 'black')

    # Title and instructions
    canvas.create_text(app.width/2.3, app.height/6,
                       text = '''
                       Begin running by clicking the space bar

                       Rhythm will calculate and display your current pace

                       Click 'Enter' when you have found a pace you are comfortable with''',
                       font = 'Visby 30 bold',
                       fill = 'lightblue')

    # Draw clicks per second on screen

    try: text = f'Current pace: {app.bpm_Tempo}'
    except: text = f'Current pace: 0'

    
    canvas.create_text(app.width/2, 2.5*app.height/4,
                       text = text,
                       font = 'Visby 75 bold ',
                       fill = 'lightyellow')



        

def intermediateFollowMode_keyPressed(app, event):
    # Register
    if event.key == 'Space': app.bpm_Tempo = estimateClicks()

    # Stop tracking and start running
    elif event.key == 'Enter' or event.key == 'Return':
        transitionToFollowMode(app)
    



       
###################################################




############### FOLLOW  MODE #####################

followMode_redrawAll = competitiveMode_redrawAll

followMode_mousePressed = competitiveMode_mousePressed

followMode_keyPressed = competitiveMode_keyPressed

followMode_keyReleased = competitiveMode_keyReleased
        
followMode_timerFired = competitiveMode_timerFired

    
            
##################################################







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




################### CONGRATULATIONS MODE ###############

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
    drawBackground(app, canvas, 'lightblue')
    app.instructionsToStart.draw(canvas)

    # Draw Title:
    canvas.create_text(app.width/2, app.height/2,
                       text = app.instructions,
                       font = 'Visby 30 bold',
                       fill = 'black')





def instructionsMode_mousePressed(app, event):        
    # If back button pressed:
    app.instructionsToStart.isPressed(event, app)
    if app.instructionsToStart.pressed:
        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'startMode'
        app.timerDelay = 20


####################################################################





    

############################ MAIN APP ###############################
def appStarted(app):
    app.mode = 'instructionsMode'
    setupInstructions(app)
    app.showingMessage = False
    app.imageX = app.width/2
    app.imageY = 0.01*app.height
    app.start = False
    app.isRightArmUp = False # boolean for movement of arms in 3D
    app.margin = 0
    app.colors = ['green', 'gray', 'yellow', 'blue', 'orange']

    app.c = 0 # index of the song playlist 
    
    app.cx = app.width/2 # x of point 3D graphics point to
    app.cy = (app.height/4) # y of point 3D graphics point to

    app.lx = app.width/2 # second 3D point
    app.ly = (1.2*app.height/4)

    app.playlist = getOriginalSongs()

    # Loading gif
    app.spritePhotoImages = loadAnimatedGif('images/blue_ncs.gif')
    app.spriteCounter = 0
    app.timerDelay = 20


    # Loading image of sky
    app.skyImage = app.loadImage('images/sky2 copy.jpg')
    app.skyImage = app.scaleImage(app.skyImage, 1.2) # rescale

    
    
    ########### CREATING ALL THE BUTTONS WE NEED #####################
      # Button to competitive
    app.buttonToCompetitive = Button('Set Goal', 0.7, app,
                                     'white', '', 'blue')
    app.buttonToCompetitive.setSize(1.5*app.width/8, app.height/1.3,
                                    3.6*app.width/8, 1.2*app.height/1.3)

      # Button to follow
    app.buttonToFollow = Button('Adaptive', 0.32, app,
                                'white', '', 'blue')
    app.buttonToFollow.setSize(4.5*app.width/8, app.height/1.3,
                               6.5*app.width/8, 1.2*app.height/1.3)
    
      # Button to back
    app.backButton = Button('BACK', 0.2, app, 'white', 'blue', 'blue')
    app.backButton.setSize(0.88*app.width, 0.91*app.height,
                                          0.98*app.width, 0.98*app.height)

      # Button intermediate to competitive
    app.intermediateToCompetitive = Button('NEXT', 0.2, app, 'white', '', 'blue')
    app.intermediateToCompetitive.setSize(0.88*app.width, 0.90*app.height,
                                          0.98*app.width, 0.97*app.height)

    # Button instructions to start
    app.instructionsToStart = Button('NEXT', 0.2, app, 'black', '', 'black')
    app.instructionsToStart.setSize(0.88*app.width, 0.90*app.height,
                                          0.98*app.width, 0.97*app.height)

      
    ##################################################################

    
    
    ########### CREATING ALL THE COUNTERS WE NEED #####################
      # Pace Counter
    app.paceCounter = Counter('Pace: ', 1, 'black', 'lightblue', app, 0.5, '')
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
    app.distanceTextBox = TextBox(app, "Distance goal (meters) : ", 0.5, 'lightblue', 'black')
    app.distanceTextBox.setSize(1.5*app.width/20, app.height/3.5,
                                1.5*10*app.width/20, 1.5*app.height/3.5)

    
    app.timeTextBox = TextBox(app, "Time goal (minutes) : ", 0.5, 'lightyellow', 'black')
    app.timeTextBox.setSize(1.5*app.width/20, 1.5*app.height/3.5,
                            1.5*10*app.width/20, 1.4*1.5*app.height/3.5)

    app.heightTextBox = TextBox(app, "Height (meters) : ", 0.5, 'lightgreen', 'black')
    app.heightTextBox.setSize(1.5*app.width/20, 2.2*app.height/3.5,
                              1.5*10*app.width/20, 1.6*1.5*app.height/3.5)

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
    app.r, app.g, app.b = app.rgbForm.getpixel((550, 580))  

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

    # By defuault, we set right arm to be up and left arm down
    app.currentRightArm = app.rightArmUp
    app.currentLeftArm = app.leftArmDown



    # # Creating coins
    app.COINS = AllCoins(app)
    app.currentCoin = app.COINS.coins[randint(0, len(app.COINS.coins) - 1)]
    # app.currentCoin = app.COINS.coins[0]
    
                
    
runApp(width = 1160, height = 800)
