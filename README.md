# 4-Channel Audio Parser for the Zoom H4n Portable Digital Recorder

The Zoom H4n is a portable digital recorder that has the ability to record 4 audio tracks at once. However, when in '4 track mode', it counterintuitively does not record 4 separate mono tracks, instead it records 2 stereo tracks (a line stereo file and a microphone stereo file). When preparing the session's recordings for processing in a DAW, one must therefore bear with the tedium of going through each stereo track, spliting them into mono tracks, and then naming the files as appropriate. I usually normalise each mono file as well, which further adds to the tedium.

This script introduces some automation, exploiting the H4n's naming convention of 4CHxxxI for the line input stereo file, and 4CHxxxM.wav for the microphone stereo file (7th character of the filename identifies it as a line input or microphone input).

## Usage
First, examine one of the session's files to establish the content of the 'I' (instrument/line) and 'M' (microphone) files.

For example, H4n will record, say, take 037 in two stereo files, 4CH037M.wav (microphone) and 4CH037I.wav (instrument/line).

Open 4CH037M.wav and 4CH037I.wav in e.g. Audacity to figure out which track is on which side of these stereo files. Write the track assignments on a piece of paper, e.g.:

*4CHxxxM.wav*  
Mic L: Female Vocals  
Mic R: Male Vocals  

*4CHxxxI.wav*  
Instrument/Line 1: Piano  
Instrument/Line 2: Bass  

(Note that with the H4n's line/instrument inputs as labelled on the device, line 1 is on the left side of the stereo file, line 2 is on the right.)

Then, run the script (placed in the same folder as all your recording session's files):

    python h4n-4ch-audio-parser.py

It will prompt you for what you just wrote on your piece of paper above, after which all the files will be split, normalised (to -32 dBFS), and named appropriately, ready for the DAW.

## Dependencies
Pydub (which in turn requires ffmpeg).

## The Future
* Using some sort of spectral analysis to establish what instruments are on each track (this would only work if each track had good isolation)
* Reading the track assignments from a file instead of getting them from prompts
* Either prompting for the normalisation level, or reading it from a file
* Suggestions?