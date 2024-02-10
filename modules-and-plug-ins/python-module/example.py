# need scikits audiolab for reading audio files
# from scikits.audiolab import wavread
import pysndfile

def wavread(filename):
  last = None
  first = 0
  hdl = pysndfile.PySndfile(filename, 'r')
  try:
    fs = hdl.samplerate()
    enc = hdl.encoding_str()
    nf  = hdl.seek(first, 1)
    if not nf == first:
        raise IOError("Error while seeking at starting position")
    if last is None:
        nframes = hdl.frames() - first
        data    = hdl.read_frames(nframes)
    else:
        data    = hdl.read_frames(last)
  finally:
    hdl.close()
  return data, fs, enc

# import numpy (needed to convert stereo audio to mono)
import numpy as np

# need to import btrack, our beat tracker
import btrack

# set the path to an audio file on your machine
audioFilePath = "/data/audio.wav"

# read the audio file
audioData, fs, enc = wavread (audioFilePath)     # extract audio from file

# convert to mono if need be
if (audioData[0].size == 2):
    print( "converting to mono")
    audioData = np.average (audioData, axis = 1)

# ==========================================    
# Usage A: track beats from audio            
beats = btrack.trackBeats (audioData)    
print(beats)

# ==========================================
# Usage B: extract the onset detection function
onsetDF = btrack.calculateOnsetDF (audioData)         

# ==========================================
# Usage C: track beats from the onset detection function (calculated in Usage B)
ODFbeats = btrack.trackBeatsFromOnsetDF (onsetDF)
print(ODFbeats)
