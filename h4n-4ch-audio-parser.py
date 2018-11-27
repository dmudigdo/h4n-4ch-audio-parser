#
# The Zoom H4n Digital Audio Recorder has a 4-channel recording mode. In this mode,
# the H4n produces two stereo files: 4CHxxxI.wav (a stereo file containing
# the line inputs) and 4CHxxxM.wav (a stereo file containing the stereo mic inputs).
#
# This script prompts for what was connected to the H4n inputs, and then scans the
# folder for the 4CH files. For each 4CH file, these stereo files are split and
# normalised. Then, the corresponding suffix is added to the filename.
#
# E.g. if during the recording the H4n mic inputs were conneted to male voice and
# female voice, and the line inputs were connected to uke and bass, run the script 
# in a folder containing the H4n 4CH files. When prompted, enter 'MaleVoice',
# 'FemaleVoice', 'Uke' and 'Bass'. The resulting files will be:
#
# 4CHxxxM_MaleVoice.wav
# 4CHxxxM_FemaleVoice.wav
# 4CHxxxI_Uke.wav
# 4CHxxxI_Bass.wav
#
# (All normalised mono files, ready for the DAW)
  

import os
from pydub import AudioSegment

def match_target_amplitude(sound, target_dBFS):
# function that does the rms normalising,
# courtesy of https://github.com/jiaaro/pydub/issues/90
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


# MAIN

# what is on mic L?
mic_L = raw_input("what is on mic L?")

# what is on mic R?
mic_R = raw_input("what is on mic R?")

# what is on line 1 (L)?
lin_1 = raw_input("what is on line 1 (L)?")

# what is on line 2 (R)?
lin_2 = raw_input("what is on line 2 (R)?")

# scan directory
wav_files = os.listdir('.')

for wav_file in wav_files:
    print "processing " + wav_file    


    f_name = os.path.splitext(wav_file) 

# validate it is a .wav
    if f_name[1] != ".wav":
        print "it's not a .wav file, next please..."
        continue
        
# if it is. wav, open the file
    stereo_audio = AudioSegment.from_file(wav_file,"wav")

# validate it is a stereo file (to prevent non-stereo splitting crash)
    if  stereo_audio.channels != 2:
        print "it's not a stereo file, next please..."
        continue

#    Check if it is M (Mic) or I (Inst i.e. line)
    if wav_file[6] == "M":
        suffix_L = mic_L
        suffix_R = mic_R

    elif wav_file[6] == "I":
        suffix_L = lin_1
        suffix_R = lin_2
    else:
# if wav_file[6] is neither 'M' nor 'I', something's wrong with the filename
        print "something's wrong with the filename, next..."
        continue
    print "suffix_L, suffix_R:" + suffix_L + " " + suffix_R

# split the file
    split_stereo_audio = stereo_audio.split_to_mono()

# Process the left channel:

# Normalise
    normalised_mono = match_target_amplitude(split_stereo_audio[0], -32.0)

# Construct the new L filename, adding suffix_L to identify
    new_track_name = f_name[0] + "_" + suffix_L + ".wav"

# Export this mono file
    normalised_mono.export(new_track_name, format="wav")
    print new_track_name + " successfully extracted and written"

# Process the right channel:

# Normalise
    normalised_mono = match_target_amplitude(split_stereo_audio[1], -32.0)

# Construct the new R filename, adding suffix_R to identify
    new_track_name = f_name[0] + "_" + suffix_R + ".wav"

# Export this mono file
    normalised_mono.export(new_track_name, format="wav")
    print new_track_name + " successfully extracted and written"

# end scan
 
# END