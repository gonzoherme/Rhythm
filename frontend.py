from cmu_112_graphics import *
from tkinter import *
import time
from backend import *
from random import randint
import time
from PIL import Image, ImageTk, ImageSequence
# import module_manager
# module_manager.review()


######################### BUTTONS ##################

class Button():
    def __init__(self, name, buttonNum, app):
        self.name = name
        self.buttonNum = buttonNum
        self.setSize(app)
        self.pressed = False

    def setSize(self, app):
        self.centerButtonX = app.width - app.width/8
        buttonWidth = app.width/5
        buttonHeight = app.height // 20
        self.fontSize = app.height // 100
        self.topLeftX = self.centerButtonX - buttonWidth/2
        self.bottomRightX = self.centerButtonX + buttonWidth/2
        self.fontSize = app.width // 100
        if self.buttonNum >= 0:
            self.topLeftY = buttonHeight/2 + self.buttonNum * buttonHeight * 3/2
            self.bottomRightY = buttonHeight * 3/2 + self.buttonNum * buttonHeight * 3/2
        else:
            self.buttonNum += 1
            self.topLeftY = app.height - buttongHeight * 3/2 + self.buttonNum * buttonHeight * 3/2
            self.bottomRightY = app.height - buttonHeight/2 + self.buttonNum*buttonHeight

    def setText(self, text):
        self.text = text


        def press(self, event, app):
            # Button Changing State
            if (self.topLeftX < event.x < self.bottomRightX and
                self.topLeftY < event.y < self.bottomRightY):
                self.pressed = True
            else:
                self.pressed = False
            if not self.pressed:
                return

        def draw(self, canvas):
            if self.pressed:
                fill = 'white'
            else:
                fill = 'gray'

            canvas.create_rectangle(self.topLeftX, self.topLeftY,
                                    self.bottomRightX, self.bottomRightY,
                                    fill = fill)

            canvas.create_text(self.centerButtonX, self.centerButtonY,
                               text = self.text,
                               fill = 'black',
                               font = f'Visby {self.fontSize} bold')
                

##################################################


########## MODEL ################
def appStarted(app):
    ################### START SCREEN ################
    app.margin = 0
    app.screen = 'start screen'
    # you don't add songs, when you start the app, it reads all the names of the files (songs) in the folder and appends to the list, so you automatically have all your songs
    app.songs = getSongs()
    app.pace = 0

    # Competitive button
    app.compBounds = [app.width/8, app.height/3.5, 7*app.width/8, 1.5*app.height/3.5]
  
    # YOP button
    app.YOPBounds = [app.compBounds[0], app.compBounds[1] + 1.2*app.height/5, app.compBounds[2], app.compBounds[3] + 1.2*app.height/5]

    # Back button
    app.backBounds = [0.7*app.width, 0.9*app.height, 0.9*app.width, 0.95*app.height]

    ###############################################################


    ###################### COMPETITIVE SCREEN #####################    
    app.counterDisplayBounds = [app.width/3, app.height/3, 2*app.width/3, 2*app.height/3]

    # Bounds Increase Pace
    app.upPaceBounds = [1.6*(app.width/3 + app.width/10), app.height/3, 2*(app.width/3 + app.width/10), 1.4*app.height/3]

    # Bounds Decrease Pace
    app.downPaceBounds = [1.6*(app.width/3 + app.width/10), 1.6*app.height/3, 2*(app.width/3 + app.width/10), 2*app.height/3]

    
    ###############################################################
    
    # app.songs = [list of songs] each song: [x0, y0, x1, y1, song Display name, song file name]

# NOTE: at the top of the page, we need to add two counters, one for height and one for speed, and next to each of them, and up arrow and a down arrow rectangles. So that the user can click on any of them to increase speed of song



        
        

    
######### CONTROLLERS #############

def clickedRegion(event, arbitraryBounds):
    if (event.x >= arbitraryBounds[0] and event.x <= arbitraryBounds[2]) and (event.y <= arbitraryBounds[3] and event.y >= arbitraryBounds[1]):
        return True
    else:
        return False
    

def mousePressed(app, event):
    # START SCREEN
    if app.screen == 'start screen':
        # Go to competitive mode
        if clickedRegion(event, app.compBounds):
            time.sleep(0.1) # delay used to simulate button friction
            app.screen = 'competitive screen'

        # Go to your own pace mode
        elif clickedRegion(event, app.YOPBounds):
            time.sleep(0.1)
            app.screen = 'your own pace screen'            


    # COMPETITIVE MODE
    elif app.screen == 'competitive screen':

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
        if clickedRegion(event, app.backBounds):
            time.sleep(0.1)
            app.screen = 'start screen'
        


    # YOUR OWN PACE MODE
    elif app.screen == 'your own pace screen':
        if clickedRegion(event, app.backBounds):
            time.sleep(0.1)
            app.screen = 'start screen'



def keyPressed(app, event):
    # if any key is pressed, automatically highlight first song, up and down arrows will highlight next song, etc. Set boundaries for highest and lowest songs. If d is clicked "and" one of the rectangles is highlighted, i.e. slightly different color from black, then remove that song from app.songs

    pass

########## VIEW ##################
def drawBackground(app, canvas):
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, app.height - app.margin, fill = 'black', outline = 'black', width = 25)



def drawStartScreen(app, canvas):
    drawBackground(app, canvas)
    # Title
    canvas.create_text(app.width/2, app.height/10, text = 'rhythm', font = 'Visby 50 bold', fill = 'lightgreen')
    
    # Draw competitive button
    # Rectangle
    canvas.create_rectangle(app.compBounds[0], app.compBounds[1], app.compBounds[2], app.compBounds[3], width = 2, fill = 'orange')
    #Text
    canvas.create_text((app.compBounds[0] + app.compBounds[2])/2, (app.compBounds[1] + app.compBounds[3])/2,  text = 'Competitive', font = f'Cambria {int(app.width/12)} bold', fill = 'white')

    
    # Draw YOP button
    # Rectangle
    canvas.create_rectangle(app.YOPBounds[0], app.YOPBounds[1], app.YOPBounds[2], app.YOPBounds[3], width = 2, fill = 'green')
    # Text
    canvas.create_text((app.YOPBounds[0] + app.YOPBounds[2])/2, (app.YOPBounds[1]+app.YOPBounds[3])/2,  text = 'Your Own Pace', font = f'Cambria {int(app.width/12)} bold', fill = 'white')




    
def drawBackButton(app, canvas):
    # Draw Button
    canvas.create_rectangle(app.backBounds[0], app.backBounds[1], app.backBounds[2], app.backBounds[3])

    # Draw text
    canvas.create_text((app.backBounds[0] + app.backBounds[2])/2, (app.backBounds[1]+app.backBounds[3])/2,  text = 'BACK', font = 'Cambria 20 bold', fill = 'white')



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

    
def drawCompetitiveScreen(app, canvas):
    # Main
    drawBackground(app, canvas)
    drawBackButton(app, canvas)
    drawPaceCounter(app, canvas)

    # # Title
    # canvas.create_text(app.width/2, app.height/10, text = 'competitive', font = 'Visby 50 bold', fill = 'white')

    
def drawYOPScreen(app, canvas):
    # Main
    drawBackground(app, canvas)
    drawBackButton(app, canvas)

    # # Title
    # canvas.create_text(app.width/2, app.height/10, text = 'your own pace', font = 'Visby 42 bold italic', fill = 'white')
    


    
def redrawAll(app,canvas):

    if app.screen == 'start screen':        
        drawStartScreen(app, canvas)
        
    elif app.screen == 'competitive screen':
        drawCompetitiveScreen(app, canvas)

    elif app.screen == 'your own pace screen':
        drawYOPScreen(app, canvas)


        
runApp(width = 400, height = 600)
