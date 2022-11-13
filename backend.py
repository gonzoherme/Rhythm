import librosa # audio file management
import os # to get names of files in a directory
from pydub import AudioSegment # to play an audio file
from pydub.playback import play # to play an audio file
from scipy.io import wavfile
from tkinter import *
import subprocess, threading, time




# Song playlist initialization
def getSongs():
    dir_path = r'/Users/gonzalodehermenegildo/Desktop/Projects/Rhythm/songs'
    file_names = os.listdir(dir_path) # list file and directories
    file_names.remove('.DS_Store') # remove mac os file

    playlist = [ ]
    for song in file_names:
        # only get name of song, remove '.wav' ending
        name = song[:-4]
        name = Song('songs/'+ song)
        playlist.append(name)
    return playlist



# Gif playing: code obtained directly from 112 notes Advanced Tkinter
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

    # def getBPM(self):
    #     
    #     
    #     y, sr = librosa.load(self.path)
    #     tempo, beat_frames = librosa.beat.beat_track(y = y, sr = sr)
    #     return tempo, y, sr


    # ratio we multiply the tempo by
    def changeTempo(self, ratio):
        # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
        #sr is the sample rate (number of samples per second)
        # y, sr = librosa.load('songs/' + filename)
        
        # replace old audio file with new created one
        wavfile.write(self.path, int(ratio*self.sr), self.y)

    
    




## Ideas:
# Top Down design: the first thing I need to write is simply the program that gets a song and increases or decreases its rythm

# We need to create a folder in which to store the mp3 files that the user uploads, and keep the right order. We can also display a queue on screen that the user can edit. The order of the files in the folder doesn't matter, what matters is a list that we have with the order of songs queued, with each item the name of the title of each mp3








 
    
    
                  
# playlist = getSongs()
# print(playlist)

# changeTempo('sample.wav', 4, playlist['sample.wav'][1], playlist['sample.wav'][2])



