######################### COUNTERS ##############################

# Button built basing upon the button presented in Mini-Lecture Advanced Tkinter
class Counter():
    def __init__(self, magnitude, initValue, textColour, fill, app, magnifier, unit):
        self.value = initValue
        self.magnitude = magnitude
        self.textColour = textColour
        self.fill = fill
        self.magnifier = magnifier
        self.unit = unit

        
    def setSize(self, topLeftX, topLeftY, bottomRightX, bottomRightY):  
        # corner point coordinates
        self.topLeftX = topLeftX
        self.topLeftY = topLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY

        # center points
        self.centerCounterX = int((self.topLeftX + self.bottomRightX)/2)
        self.centerCounterY = int((self.topLeftY + self.bottomRightY)/2)


        # font
        self.fontSize = int(self.magnifier*(self.centerCounterX/5))


           
        
    def draw(self, canvas):            
        # Draw rectangle
        canvas.create_rectangle(self.topLeftX, self.topLeftY,
                                self.bottomRightX, self.bottomRightY,
                                fill = self.fill)
        # Draw text
        canvas.create_text(self.centerCounterX, self.centerCounterY,
                           text = self.magnitude + f'{self.value} {self.unit}',
                           fill = self.textColour,
                           font = f'Visby {self.fontSize} bold')
                
#######################################################################






######################### BUTTONS ####################################

# Button built basing upon the button presented in Mini-Lecture Advanced Tkinter
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
            # self.fill = 'gray'

        else:
            self.pressed = False
            # self.fill = self.fill

           
        
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

###########################################################################





######################### TEXT BOX ######################################
class TextBox():        
    def __init__(self, app, text, proportion, textColour, fill):
        self.text = text + ' '
        self.proportion = proportion
        self.textColour = textColour
        self.fill = fill
        self.pressed = False

        
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
        self.fontSize = int(self.proportion*(self.centerButtonX/5))


    def isPressed(self, event, app):
        # Button Changing State
        if (self.topLeftX < event.x < self.bottomRightX and
            self.topLeftY < event.y < self.bottomRightY):
            self.pressed = True                            

        else:
            self.pressed = False

                   
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


###########################################################################        



########################## GRAPHICS CLASSES ###############################
class Road(): #make a polygon, like triangle-like!!! Not two lines
    def __init__(self, fill, outlineColor):
        self.fill = fill
        self.outlineColor = outlineColor


    def setSize(self, bottomLeftX, bottomLeftY, bottomRightX, bottomRightY):
        self.bottomLeftX = bottomLeftX
        self.bottomLeftY = bottomLeftY
        self.bottomRightX = bottomRightX
        self.bottomRightY = bottomRightY

        
    def draw(self, app, canvas):
        # draw lines connecting both points
        canvas.create_polygon(self.bottomLeftX, self.bottomLeftY, app.cx,
                              app.cy, self.bottomRightX, self.bottomRightY,
                              outline = self.outlineColor,
                              fill = self.fill)


    

    
