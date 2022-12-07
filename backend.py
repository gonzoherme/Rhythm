from pydub import AudioSegment # to play an audio file
from pydub.playback import play # to play an audio file
from scipy.io import wavfile
from tkinter import *
from random import randint, shuffle
import subprocess, threading, time
import librosa # audio file management
import os # to get names of files in a directory
from math import sqrt


# CITING MULTIMEDIA USED
# Music citation: all .wav files obtained from https://pixabay.com/music/search/wav/
# https://www.ee.columbia.edu/~dpwe/sounds/music/africa-toto.wav

# Gif citation: https://giphy.com/nocopyrightsounds

# Sky image citation: 
# https://wallhere.com/en/wallpaper/113569




# Song playlist initialization
def getOriginalSongs():
    dir_path = r'/Users/gonzalodehermenegildo/Desktop/Projects/Rhythm/songs/originals'
    file_names = os.listdir(dir_path) # list file and directories

    # try to remove .DS_Store default mac file if there
    try: file_names.remove('.DS_Store') # remove mac os file
    except Exception: pass

    playlist = [ ]
    for song in file_names:
        # only get name of song, remove '.wav' ending
        name = song[:-4]
        name = Song('songs/originals/'+ song)
        playlist.append(name)
    return playlist


def getAlteredSongs():
    dir_path = r'/Users/gonzalodehermenegildo/Desktop/Projects/Rhythm/songs/altered'
    file_names = os.listdir(dir_path) # list file and directories
    # try to remove .DS_Store default mac file if there
    try: file_names.remove('.DS_Store') # remove mac os file
    except Exception: pass

    playlist = [ ]
    for song in file_names:
        # only get name of song, remove '.wav' ending
        name = song[:-4]
        name = Song('songs/altered/'+ song)
        playlist.append(name)
    return playlist
#####################################################








###################### SOUND CLASS ################
# Citation: Song class
# built upon code from cmu 112 Advanced Animations with Tkinter https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods    

class Song(object):
    def __init__(self, path):
        self.path = path
        self.process = None
        self.loop = False

        # Cuantitative properties
        # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
        # sr is the sample rate (number of samples per second)
        self.y, self.sr = librosa.load(self.path)
        self.tempo, self.beat_frames = librosa.beat.beat_track(y = self.y,
                                                               sr = self.sr)

        

    def isPlaying(self): return (self.process is not None)
    
    def checkProcess(self):
        # This method is run inside a separate thread
        # so the main thread does not hang while this runs.
        while self.process is not None:
            if (self.process.poll() is not None): self.process = None
            else: time.sleep(0.2)

        if self.loop: self.start(loop=True)

            
    def start(self, loop=False):
        self.stop()
        self.loop = loop
        self.process = subprocess.Popen(['afplay', self.path])  
        threading.Thread(target=self.checkProcess).start()

        
    def stop(self):
        process = self.process
        self.loop = False
        self.process = None
        if (process is not None):
            try: process.kill()
            except: pass


    # ratio we multiply the tempo by
    def changeTempo(self, desiredBPM):
        # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
        #sr is the sample rate (number of samples per second)
        # y, sr = librosa.load('songs/' + filename)

        # ratio we want to multiply by:
        ratio = desiredBPM / self.tempo

        # create copies of original songs but altered in a different directory
        path = self.path.replace('originals', 'altered') # non-destructive, doesn't affect self.path
        
        # create temporary file
        wavfile.write(path, int(ratio*self.sr), self.y)

#################################################################3



############ Pace calculator
# Citation on ratio to calculate person's stride from their height:
#https://www.livestrong.com/article/438560-the-average-stride-length-in-running/
def setRequiredParameters(app):
    app.distanceMeters = float(app.distanceTextBox.text[25:]) # In meters!!
    app.timeMinutes = float(app.timeTextBox.text[21: ]) # In minutes!!
    app.timeSeconds = app.timeMinutes*60
    app.heightMeters = float(app.heightTextBox.text[18: ])  # In meters!!

    app.timeCounter.value = app.timeSeconds
    app.strideMeters = app.heightMeters * 1.17

    numberSteps = int(app.distanceMeters/app.strideMeters)

    app.stepsPerMinute = int(numberSteps / app.timeMinutes)

    # rightFootStepsPerMinute = int(stepsPerMinute/2)
    app.paceCounter.value = app.stepsPerMinute

 

# Load Animated Gif: citation, code from 112 Animations Part 4 Notes
def loadAnimatedGif(path):
    # load first sprite outside of try/except to raise file-related exceptions
    spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
    i = 1
    while True:
        try:
            spritePhotoImages.append(PhotoImage(file=path,
                                                format=f'gif -index {i}'))
            i += 1
        except Exception as e: return spritePhotoImages


    
# Only display two decimals
def reduceDecimals(val):
    string = str(val)
    dotIndex = string.index('.')
    string = string[ : dotIndex+3]

    # add decimal 0 to end of number if only one decimal point
    newDotIndex = string.index('.')

    if len(string[newDotIndex:]) < 3: string += '0'

    return string
    

## Drawing background function
def drawBackground(app, canvas, fill):
    canvas.create_rectangle(app.margin, app.margin,
                            app.width - app.margin,
                            app.height - app.margin,
                            fill = fill, outline = 'black',
                            width = 25)


# Reset all
def resetAll(app):
    app.distanceTextBox.text = "Distance goal (meters) : "
    app.timeTextBox.text = "Time goal (minutes) : "
    app.heightTextBox.text = "Height (meters):  "
    app.timerDelay = 20


# For rgb strings    
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'





####################### CLICKS PER SECOND METER #####################

time_frames = []
def estimateClicks():
    global time_frames
    time_frames.append(time.time())
    length_list = len(time_frames)
    N = 6
    if length_list > 1:
        # If two times are considerably far from eachother, we throw away the former times, only leaving the last one, i.e., resetting timer

        if time_frames[-1] - time_frames[-2] > 2:
            time_frames = time_frames[-1:]
            tempo = 0
            return tempo

        else:
            if length_list < N:
                interval = (time_frames[-1] - time_frames[0]) / (length_list - 1)
            else:
                interval = (time_frames[-1] - time_frames[-N]) / (N - 1)
            tempo = int(60/interval)

            return tempo
    else:
        # Continue to click until more than 1 entry
        tempo = 0
        return tempo

#####################################################################



########## Transition to Competitive #######
def transitionToCompetitive(app):
    
    # Reset distance from previous session
    if app.distanceCounter.value != 0: app.distanceCounter.value = 0
        
    # Setup all the required data
    setRequiredParameters(app)
    
    time.sleep(0.1) # delay used to simulate button friction
    app.mode = 'competitiveMode'
    app.timerDelay = 1


    # Set the speed for our rhythm marking coins
    x1, x0, y1, y0 = 734, 630, 513, 300
    distanceOneCoinRun = sqrt((x1-x0)**2 + (y1-y0)**2) # point (x0,y0) to (x1,y1)
    print(f'Distance: {distanceOneCoinRun}')
    timePerStep = 60/app.paceCounter.value # seconds
    # print(f'Time: {timePerStep}')
    app.miliseconds = 0
    speedCoin = distanceOneCoinRun / timePerStep
    app.coinDisplacement = 0.0422*speedCoin
    print(app.coinDisplacement)

    
    # Changing songs to set pace
    for song in app.playlist: song.changeTempo(app.stepsPerMinute)

    app.playlist =  getAlteredSongs()

    # START PLAYING SONGS
    # We start to play the songs, as well as start the countdown
    app.start = True

    # Play our playlist
    # Shuffle the playlist
    shuffle(app.playlist)
    app.playlist[app.c].start()


##############################################





########## Transition to Follow mode ##########

def transitionToFollowMode(app):
        # Reset distance from previous session
        if app.distanceCounter.value != 0: app.distanceCounter.value = 0
        
        # Setup all the required data
        app.distanceMeters = 100000000
        app.timeMinutes = 1000000
        app.timeSeconds = app.timeMinutes*60
        app.timeCounter.value = 10000
        app.heightMeters = 1.83
        app.strideMeters = app.heightMeters * 1.17
        app.paceCounter.value = app.bpm_Tempo

        time.sleep(0.1) # delay used to simulate button friction
        app.mode = 'followMode'
        app.timerDelay = 1


        # Setup coin sped
        # Set the speed for our rhythm marking coins
        x1, x0, y1, y0 = 734, 630, 513, 300
        distanceOneCoinRun = sqrt((x1-x0)**2 + (y1-y0)**2) # point (x0,y0) to (x1,y1)
        timePerStep = 60/app.paceCounter.value # seconds
        app.miliseconds = 0
        speedCoin = distanceOneCoinRun / timePerStep
        app.coinDisplacement = 0.0422*speedCoin

        # Changing songs to set pace
        for song in app.playlist: song.changeTempo(app.paceCounter.value)

        app.playlist =  getAlteredSongs()

        # START PLAYING SONGS
        # We start to play the songs, as well as start the countdown
        app.start = True

        # Play our playlist
        # Shuffle the playlist
        shuffle(app.playlist)
        app.playlist[app.c].start()


################################################



# Calculate the distance if player was on track:
def onTrackDistance(app):
    app.timeRunning = app.timeSeconds - app.timeCounter.value
    app.percentageTimeOfTotal = ( app.timeRunning / app.timeSeconds )
    on_track_distance = app.percentageTimeOfTotal * app.distanceMeters
    return on_track_distance



############# DRAWING MESSAGES TO USER
def drawUserMessage(app, canvas):               
    if app.on_track:
        canvas.create_text(app.width/2, app.height/3,
                           text = app.currentOnTrackMessage,
                           font = ("Comic Sans MS", 80, "bold"),
                           fill = 'lightgreen')

    elif not app.on_track:
        canvas.create_text(app.width/2, app.height/3,
                           text = app.currentOffTrackMessage,
                           font = ("Comic Sans MS", 90, "bold"),
                           fill = 'red') 
        
            


        
################# Check if runner finished
def checkRunnerFinished(app):
    # Congrats! made the objective
    if float(app.distanceCounter.value) >= app.distanceMeters:        
        app.mode = 'congratulationsMode'
        resetAll(app)

    # print(app.distanceCounter.value)
    # print(app.timeCounter.value, f'{app.distanceCounter.value} < {app.distanceMeters}' )
    # Runner did not make the objective
    if (app.timeCounter.value <= 0 and
        int(float(app.distanceCounter.value)) < int(app.distanceMeters)):
        app.mode = 'improvementMode'


# Setup instructions
def setupInstructions(app):
    app.instructions = '''

    Rhythm is an application devoted to aiding runners in
    maintaining a desired pace through the music they listen to.

    Instructions:
    Press 'Space' to simulate each step of your run
    Use the 'Left' and 'Right' arrows to move your avatar

    Click on 'Set Goal' for Rhythm to help you achieve a
    specific running goal in terms of distance and time

    Click on 'Adaptive' to run at your own pace, and Rhythm will
    play songs in your playlist to match your running tempo
    '''



### Drawing rounded rectangles helper function
def drawRoundedRectangle(x0, y0, x1, y1, fill, r, canvas):
        # Inner rectangle
        canvas.create_rectangle(x0, y0,
                                x1, y1,
                                fill = fill, outline = fill,
                                width = 0)

        # Vertical outer rectangle
        canvas.create_rectangle(x0, y0 - r,
                                x1, y1 + (r+1),
                                fill = fill, outline = fill,
                                width = 0)

        # Horizontal outer rectangle
        canvas.create_rectangle(x0 - r, y0,
                                x1 + (r+1), y1,
                                fill = fill, outline = fill,
                                width = 0)
        
        
        # Draw round corners to smoothen out
        # Top left oval
        canvas.create_oval(x0 + r, y0 + r,
                           x0 - r, y0 - r,
                           fill = fill, outline = fill)

        # Bottom right oval
        canvas.create_oval(x1 + r, y1 + r,
                           x1 - r, y1 - r,
                           fill = fill, outline = fill)
        # Bottom left oval
        canvas.create_oval(x0 + r, y1 + r,
                           x0 - r, y1 - r,
                           fill = fill, outline = fill)
        
        # Top right oval
        canvas.create_oval(x1 + r, y0 + r,
                           x1 - r, y0 - r,
                           fill = fill, outline = fill)