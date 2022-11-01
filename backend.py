import librosa # audio file management
import os # to get names of files in a directory

from pydub import AudioSegment # to play an audio file
from pydub.playback import play # to play an audio file

from tkinter import *


def getSongs():
    # dir_path = r'/Users/gonzalodehermenegildo/Desktop/Projects/Rhythm/songs'
    # file_names = os.listdir(dir_path) # list file and directories
    # file_names.remove('.DS_Store') # remove mac os file

    # song_list = []
    # for song in file_names:
    #     tempo = getBPM(song)
    #     song_list.append([song, tempo])
    
    # return song_list
    return None
    
## Ideas:
# Top Down design: the first thing I need to write is simply the program that gets a song and increases or decreases its rythm

# We need to create a folder in which to store the mp3 files that the user uploads, and keep the right order. We can also display a queue on screen that the user can edit. The order of the files in the folder doesn't matter, what matters is a list that we have with the order of songs queued, with each item the name of the title of each mp3

def getBPM(filename):
    # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
    #sr is the sample rate (number of samples per second)
    y, sr = librosa.load('songs/' + filename)
    tempo, beat_frames = librosa.beat.beat_track(y = y, sr = sr)
    return tempo


# ratio we multiply the tempo by
def changeTempo(currentBPM, filename, ratio):
    # y is the time series: the audio signal represented as a one-dimensional numpy.ndarray
    #sr is the sample rate (number of samples per second)
    y, sr = librosa.load(filename)
    # create new audio file
    wavfile.write('songs/' + filename, int(sr*ratio), y)



    
# playlist = getSongs()
# print(playlist)


# song = AudioSegment.from_wav("songs/sample.wav")
# play(song)

    
