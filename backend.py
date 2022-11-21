import librosa # audio file management
import os # to get names of files in a directory
from pydub import AudioSegment # to play an audio file
from pydub.playback import play # to play an audio file
from scipy.io import wavfile
from tkinter import *
import subprocess, threading, time

#CITATIONS
# Music citation: all .wav files obtained from https://pixabay.com/music/search/wav/
# Gif citation: https://giphy.com/nocopyrightsounds
# Sky image citation: https://www.google.com/search?q=png+sky&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj_8pLyzb37AhXcElkFHXeiDQQQ_AUoAXoECAIQAw&biw=1440&bih=800&dpr=2#imgrc=tEtK2gCdyG43YM

# Song playlist initialization
def getOriginalSongs():
    dir_path = r'/Users/gonzalodehermenegildo/Desktop/Projects/Rhythm/songs/originals'
    file_names = os.listdir(dir_path) # list file and directories
    # try to remove .DS_Store default mac file if there
    try:
        file_names.remove('.DS_Store') # remove mac os file
    except Exception:
        pass

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
    try:
        file_names.remove('.DS_Store') # remove mac os file
    except Exception:
        pass

    playlist = [ ]
    for song in file_names:
        # only get name of song, remove '.wav' ending
        name = song[:-4]
        name = Song('songs/altered/'+ song)
        playlist.append(name)
    return playlist
#####################################################








###################### SOUND CLASS ################
# Citation: built upon code from cmu 112 Advanced Animations with Tkinter https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods    

class Song(object):
    def __init__(self, path):
        self.path = path
        self.process = None
        self.loop = False

        # Cuantitative properties
        # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
        # sr is the sample rate (number of samples per second)
        self.y, self.sr = librosa.load(self.path)
        self.tempo, self.beat_frames = librosa.beat.beat_track(y = self.y, sr = self.sr)

        

    def isPlaying(self):
        return (self.process is not None)

    
    def checkProcess(self):
        # This method is run inside a separate thread
        # so the main thread does not hang while this runs.
        while self.process is not None:
            if (self.process.poll() is not None):
                self.process = None
            else:
                time.sleep(0.2)
        if self.loop:
            self.start(loop=True)

            
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



# PLAYING GIFS
# Gif playing: code obtained directly from 112 notes Advanced Tkinter
# def loadAnimatedGif(path):
#     # load first sprite outside of try/except to raise file-related exceptions
#     spritePhotoImages = [ PhotoImage(file=path, format='gif -index 0') ]
#     i = 1
#     while True:
#         try:
#             spritePhotoImages.append(PhotoImage(file=path,
#                                                 format=f'gif -index {i}'))
#             i += 1
#         except Exception as e:
#             return spritePhotoImages


############ Pace calculator
# Citation to calculate person's stride from their height:
# https://www.livestrong.com/article/438560-the-average-stride-length-in-running/
def setRequiredParameters(app):
    app.distanceMeters = float(app.distanceTextBox.text[15:]) # In meters!!
    app.timeMinutes = int(app.timeTextBox.text[11: ]) # In minutes!!
    app.heightMeters = float(app.heightTextBox.text[8: ])  # In meters!!

    app.timeCounter.value = app.timeMinutes*60
    app.strideMeters = app.heightMeters * 1.17

    numberSteps = int(app.distanceMeters/app.strideMeters)

    app.stepsPerMinute = int(numberSteps / app.timeMinutes)

    # rightFootStepsPerMinute = int(stepsPerMinute/2)
    app.paceCounter.value = app.stepsPerMinute



    

# Only display two decimals
def reduceDecimals(val):
    string = str(val)
    dotIndex = string.index('.')
    string = string[ : dotIndex+3]

    # add decimal 0 to end of number if only one decimal point
    newDotIndex = string.index('.')

    if len(string[newDotIndex:]) < 3:
        string += '0'

    return string
    

## Drawing background function
def drawBackground(app, canvas, fill):
    canvas.create_rectangle(app.margin, app.margin, app.width - app.margin, app.height - app.margin, fill = fill, outline = 'black', width = 25)


# Reset all
def resetAll(app):
    app.distanceTextBox.text = "Distance goal: "
    app.timeTextBox.text = "Time goal: "
    app.heightTextBox.text = "Height: "
