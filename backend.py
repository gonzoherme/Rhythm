import librosa # audio file management
import os # to get names of files in a directory
from pydub import AudioSegment # to play an audio file
from pydub.playback import play # to play an audio file
from scipy.io import wavfile
from tkinter import *
import subprocess, threading, time




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
        print(self.tempo)
        

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
    def changeTempo(self, ratio):
        # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
        #sr is the sample rate (number of samples per second)
        # y, sr = librosa.load('songs/' + filename)
        
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
#https://www.scientificamerican.com/article/bring-science-home-estimating-height-walk/
def calculatePace(app):
    distanceMeters = app.distanceTextBox[9:] # In meters!!
    heightMeters = app.heightTextBox[7: ]  # In meters!!
    timeMinutes = app.timeTextBox[5: ] # In minutes!!
    strideMeters = height * 0.42

    numberSteps = int(distanceMeters/strideMeters)
    stepsPerMinute = int(timeMinutes / numberSteps)
            
    return stepsPerMinute
    
