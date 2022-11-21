import sys
print('--------------')
print(sys.executable)
print('----------------')

from cmu_112_graphics import *

def appStarted(app):
    app.spritePhotoImages = loadAnimatedGif('images/green_ncs.gif')
    app.spriteCounter = 0
    app.timerDelay = 40

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

def timerFired(app):
    app.spriteCounter = (1 + app.spriteCounter) % len(app.spritePhotoImages)

def redrawAll(app, canvas):
    photoImage = app.spritePhotoImages[app.spriteCounter]
    canvas.create_image(200, 200, image=photoImage)


runApp(width=400, height=400)
