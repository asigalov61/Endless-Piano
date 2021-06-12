# -*- coding: utf-8 -*-
"""Endless_Piano.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1lyyAnFzR0Xhi-qwh_cA5ZTcbZh0LfyQM

# Endless Piano (ver. 6.0)

***

## Endless Semi-Generative Performance Piano Music Maker

***

### Powered by tegridy-tools TMIDI & GiantMIDI Dataset https://github.com/bytedance/GiantMIDI-Piano

***

#### Project Los Angeles

#### Tegridy Code 2021

***

# Setup environment
"""

#@title Install tegridy-tools
!git clone https://github.com/asigalov61/tegridy-tools

#@title Import all needed modules

print('Loading needed modules. Please wait...')
import os
import copy

import tqdm
from tqdm import auto

import secrets
import random

if not os.path.exists('/content/Dataset'):
    os.makedirs('/content/Dataset')

os.chdir('/content/tegridy-tools/tegridy-tools')
import TMIDI

os.chdir('/content/')
print('Loading complete. Enjoy! :)')

"""# Download and load processed GiantMIDI dataset (Required)

## NOTE: Loading will take about 5 minutes and 10GB RAM
"""

#@title Download processed GiantMIDI dataset (Required)
# %cd /content/
!wget --no-check-certificate -O GiantMIDI.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118491&authkey=AKrxNM53z9DGX2Y"
!unzip -j GiantMIDI.zip

#@title Load the dataset

#@markdown NOTE: This may take a while. Please wait...
slices_length_in_miliseconds = 4000 #@param {type:"slider", min:1000, max:8000, step:1000}
overlap_notes_per_slice = 2 #@param {type:"slider", min:0, max:10, step:1}

print('=' * 70) 
print('Loading GiantMIDI Dataset. Please wait...')
print('=' * 70)
quarter_pairs1 = TMIDI.Tegridy_Any_Pickle_File_Loader('/content/GiantMIDI')
print('=' * 70)

print('Randomizing the dataset...')
random.shuffle(quarter_pairs1[0])
print('=' * 70)

print('Slicing the dataset...')
quarter_pairs = []
for qp in auto.tqdm(quarter_pairs1[0]):
  quarter_pairs.extend(TMIDI.Tegridy_Score_Slicer(qp, slices_length_in_miliseconds, overlap_notes=overlap_notes_per_slice)[0])
print('=' * 70)

print('Randomizing the score slices...')
random.shuffle(quarter_pairs)
print('=' * 70)

print('Generating score slices music features signatures...')
signatures = []
for qp in auto.tqdm(quarter_pairs):
  signatures.append(TMIDI.Tegridy_Chords_List_Music_Features(qp, st_dur_div=16, pitch_div=2, vel_div=2)) #st_dur_div=32, pitch_div=4, vel_div=4))
print('=' * 70)

print('Processing finished! Enjoy! :)')
print('=' * 70)

"""# (OPTIONAL) Process your own dataset"""

#@title Process MIDIs to special MIDI dataset with Optimus MIDI Processor

desired_dataset_name = "Endless-Piano-Music-Dataset" #@param {type:"string"}
file_name_to_output_dataset_to = "/content/Endless-Piano-Music-Dataset" #@param {type:"string"}
desired_MIDI_channel_to_process = 0 #@param {type:"slider", min:-1, max:16, step:1}
encode_MIDI_channels = False #@param {type:"boolean"}
encode_velocities = False #@param {type:"boolean"}
chordify_input_MIDIs = False #@param {type:"boolean"}
melody_conditioned_encoding = False #@param {type:"boolean"}
melody_pitch_baseline = 60 #@param {type:"slider", min:1, max:127, step:1}
time_denominator = 1 #@param {type:"slider", min:1, max:20, step:1}
chars_encoding_offset = 33 #@param {type:"number"}
slices_length_in_miliseconds = 4000 #@param {type:"slider", min:1000, max:8000, step:1000}
overlap_notes_per_slice = 2 #@param {type:"slider", min:0, max:10, step:1}
perfect_timings = True #@param {type:"boolean"}

print('=' * 70)
print('TMIDI Optimus Processor')
print('Starting up...')
print('=' * 70)

###########

average_note_pitch = 0
min_note = 127
max_note = 0

files_count = 0

ev = 0
notes_list_f = []
chords_list_f = []
melody_list_f = []

chords_list = []
chords_count = 0

melody_chords = []
melody_count = 0

TXT = ''
melody = []
chords = []
bf = 0
###########

print('Loading MIDI files...')
print('This may take a while on a large dataset in particular.')

dataset_addr = "/content/Dataset/"
os.chdir(dataset_addr)
filez = list()
for (dirpath, dirnames, filenames) in os.walk(dataset_addr):
    filez += [os.path.join(dirpath, file) for file in filenames]
print('=' * 70)

# Stamping the dataset
print('Stamping the dataset...')

TXT_String = 'DATASET=' + str(desired_dataset_name) + chr(10)
TXT_String += 'CHARS_ENCODING_OFFSET=' + str(chars_encoding_offset) + chr(10)
TXT_String += 'LEGEND=STA-DUR-PTC'
if encode_velocities:
  TXT_String += '-VEL'
if encode_MIDI_channels:
  TXT_String += '-CHA'
TXT_String += chr(10)

pf = []
kar_ev = []
pxp_ev = []

print('=' * 70)

print('Processing MIDI files. Please wait...')

for f in tqdm.auto.tqdm(filez):
  try:
    fn = os.path.basename(f)

    fnn = fn
    fn1 = fnn.split('.')[0]
    fn3 = ['MIDI']

    TXT, melody, chords = TMIDI.Optimus_MIDI_TXT_Processor(f, 
                                                           line_by_line_output=False, 
                                                           chordify_TXT=chordify_input_MIDIs, 
                                                           output_MIDI_channels=encode_MIDI_channels, 
                                                           char_offset=chars_encoding_offset, 
                                                           dataset_MIDI_events_time_denominator=time_denominator, 
                                                           output_velocity=encode_velocities, 
                                                           MIDI_channel=desired_MIDI_channel_to_process,
                                                           MIDI_patch=range(0,127), 
                                                           melody_conditioned_encoding=melody_conditioned_encoding,
                                                           melody_pitch_baseline=melody_pitch_baseline,
                                                           song_name=fn1, 
                                                           perfect_timings=perfect_timings)
    chords_list_f.append(chords)

    melody_list_f.append(melody)

    pf.append([fn1, f.split('/')[-2], fn3])


    files_count += 1

  except KeyboardInterrupt:
    print('Exiting...Saving progress...')
    break

  except:
    bf += 1
    print('Bad MIDI:', f)
    print('Count:', bf)
    
    continue

print('Task complete! :)')
print('=' * 70)

print('Number of processed dataset MIDI files:', files_count)
print('First chord event:', chords_list_f[0][0], 'Last chord event:', chords_list_f[-1][-1]) 
print('First melody event:', melody_list_f[0][0], 'Last Melody event:', melody_list_f[-1][-1])
print('=' * 70)

# Dataset
print('Finalizing the dataset...')
MusicDataset = [chords_list_f, melody_list_f, kar_ev, filez, pf, bf, files_count]
print('=' * 70)

print('Randomizing the dataset...')
random.shuffle(chords_list_f)
print('=' * 70)

quarter_pairs1 = [chords_list_f]

print('Slicing the dataset...')
quarter_pairs = []
for d in auto.tqdm(quarter_pairs1[0]):
  quarter_pairs.extend(TMIDI.Tegridy_Score_Slicer(d, slices_length_in_miliseconds, overlap_notes=overlap_notes_per_slice)[0])
print('=' * 70)

print('Randomizing the score slices...')
random.shuffle(quarter_pairs)
print('=' * 70)

print('Generating score slices music features signatures...')
signatures = []
for qp in auto.tqdm(quarter_pairs):
  signatures.append(TMIDI.Tegridy_Chords_List_Music_Features(qp, st_dur_div=16, pitch_div=2, vel_div=2)) #st_dur_div=32, pitch_div=4, vel_div=4))
print('=' * 70)

TMIDI.Tegridy_Pickle_File_Writer(MusicDataset, file_name_to_output_dataset_to)

"""# Generate Endless Classical Piano Music"""

#@title (RECOMMENDED) Generate music with the overlapping score slices matching

#@markdown NOTE: If nothing is being generated or if the song is too short: re-run the generator.

#@markdown NOTE: Broader slices match types == slower/more plagiarized output, so you will need to find just the right settings for your dataset and output preferences.

number_of_slices_to_try_to_generate = 20 #@param {type:"slider", min:1, max:100, step:1}
slices_match_type = "pitches_durations_and_beat" #@param ["pitches_only", "pitches_and_durations", "pitches_and_beat", "pitches_durations_and_beat", "pitches_durations_and_velocities", "pitches_durations_velocities_and_beat", "pitches_durations_velocities_beat_and_channel"]
overlap_notes = overlap_notes_per_slice

print('=' * 70)
print('Endless Piano')
print('=' * 70)

print('Starting up...')
print('=' * 70)

print('Number of MIDI compositions in the dataset:', len(quarter_pairs1[0]))
print('Number of compositions scores slices in the dataset:', len(quarter_pairs))
print('=' * 70)

print('Slices matching type:', slices_match_type)
print('=' * 70)

c = 2
total_notes = 0

idx = secrets.randbelow(len(quarter_pairs))
song = []
song.append(quarter_pairs[idx])

print('Starting slice index:', idx, 'out of', len(quarter_pairs))
print('=' * 70)

print('Starting main search...')
print('=' * 70)

for i in auto.tqdm(range(number_of_slices_to_try_to_generate)):
  
  try:  
    p1 = [y[4] for y in song[-1][-overlap_notes:]]
    d1 = [int(y[2] / 128) for y in song[-1][-overlap_notes:]]
    ch1 = [int(y[3]) for y in song[-1][-overlap_notes:]]
    v1 = [int(y[5] / 8) for y in song[-1][-overlap_notes:]]
    
    tds1 = [int(abs(song[-1][-overlap_notes:][i-1][1]-song[-1][-overlap_notes:][i][1]) / 128) for i in range(1, len(song[-1][-overlap_notes:]))]
    if len(tds1) != 0: atds1 = int(sum(tds1) / len(tds1))
    
    for qp in quarter_pairs:

          p2 = [y[4] for y in qp[:overlap_notes]]
          d2 = [int(y[2] / 128) for y in qp[:overlap_notes]]
          v2 = [int(y[5] / 8) for y in qp[:overlap_notes]]
          ch2 = [int(y[3]) for y in qp[:overlap_notes]]
          
          tds2 = [int(abs(qp[:overlap_notes][i-1][1]-qp[:overlap_notes][i][1]) / 128) for i in range(1, len(qp[:overlap_notes]))]
          if len(tds2) != 0: atds2 = int(sum(tds2) / len(tds2))


          if slices_match_type == 'pitches_only':
            if p1 == p2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break
          
          if slices_match_type == 'pitches_and_durations':
            if p1 == p2 and d1 == d2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break

          if slices_match_type == 'pitches_and_beat':
            if p1 == p2 and atds1 == atds2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break

          if slices_match_type == 'pitches_durations_and_velocities':
            if p1 == p2 and d1 == d2 and v1 == v2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break
          
          if slices_match_type == 'pitches_durations_and_beat':
            if p1 == p2 and d1 == d2 and atds1 == atds2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break
          
          if slices_match_type == 'pitches_durations_velocities_and_beat':
            if p1 == p2 and d1 == d2 and v1 == v2 and atds1 == atds2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break

          if slices_match_type == 'pitches_durations_velocities_beat_and_channel':
            if p1 == p2 and d1 == d2 and v1 == v2 and atds1 == atds2 and ch1 == ch2:
              if qp[overlap_notes:] not in song:            
                song.append(qp[overlap_notes:])
                total_notes += len(song[-1])
                print('Found', c, 'slices /', total_notes, 'notes...')
                c += 1
                break

    if c == i + 1:
      print('=' * 70)
      print('Generator exhausted. Stopping...')
      break
  
  except KeyboardInterrupt:
    print('=' * 70)
    print('Keyboard interrupt requested...')
    print('Saving progress and writing resulting MIDI...')
    break

print('=' * 70)

if c >= i + 1:

  print('Finalizing resulting song...')
  print('=' * 70)
  song1 = []
  for s in song:
    song1.extend(s)
  song1 = [s for s in song1 if type(s) == list]

  print('Analyzing generated song...')
  ptime = 0
  count = 1
  ptime = song1[0][1]
  for s in song1:
    if abs(s[1] - ptime) > 1000:
      count += 1
    ptime = s[1]
  print('Song has', count, 'unique pieces.')
  if count < 2:
    print('PLAGIARIZM WARNING: Your composition is most likely plagiarizm')
  print('=' * 70)

  print('Adding unique pieces labels to the song...')
  song2 = []
  ptime = song1[0][1]
  song2.append(['text_event', song1[0][1], str(song1[0])])
  for s in song1:
    if abs(s[1] - ptime) > 1000:
      song2.append(['text_event', s[1], str(s)])
      song2.append(s)
    else:
      song2.append(s)
    ptime = s[1]
  print('=' * 70)

  print('Recalculating songs timings...')
  song3 = TMIDI.Tegridy_Timings_Converter(song2)[0]
  print('=' * 70)

  print('Total song length:', len(song3))
  print('=' * 70)

  comp_numb = sum([y[4] for y in song3 if y[0] == 'note'])
  comp_length = len(song3)
  print('Endless Piano Composition #:', comp_numb, '-', comp_length)
  print('=' * 70)

  stats = TMIDI.Tegridy_SONG_to_MIDI_Converter(song3,
                                              output_signature='Endless Piano',
                                              output_file_name='/content/Endless-Piano-Music-Composition', 
                                              list_of_MIDI_patches=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
                                              track_name='Composition #:' + str(comp_numb) + '-' + str(comp_length))
  print('=' * 70)

#@title (OPTIONAL) Generate music with score slices music features signatures matching

#@markdown NOTE: If nothing is being generated or if the song is too short: re-run the generator.

#@markdown NOTE: Sometimes the generator gets stuck. In such case, simply re-run the generator several times until it works.

number_of_slices_to_try_to_generate = 20 #@param {type:"slider", min:1, max:100, step:1}
overlap_notes = overlap_notes_per_slice

print('=' * 70)
print('Endless Piano')
print('=' * 70)

print('Starting up...')
print('=' * 70)

print('Number of MIDI compositions in the dataset:', len(quarter_pairs1[0]))
print('Number of compositions scores slices in the dataset:', len(quarter_pairs))
print('=' * 70)

c = 2
total_notes = 0

idx = secrets.randbelow(len(quarter_pairs))
song = []
song.append(quarter_pairs[idx])

print('Starting slice index:', idx, 'out of', len(quarter_pairs))
print('=' * 70)

print('Starting main search...')
print('=' * 70)

c = 2
total_notes = 0

sig = signatures[secrets.randbelow(len(signatures))]

song = []
song.append(quarter_pairs[signatures.index(sig)][overlap_notes_per_slice:])
for i in auto.tqdm(range(number_of_slices_to_try_to_generate)):
  try:
    for s in signatures:

      s1 = sig[6:11]
      s2 = s[6:11]
      if s1 == s2 and signatures.index(s) != signatures.index(sig):
        if quarter_pairs[signatures.index(s)][overlap_notes_per_slice:] not in song:
          song.append(quarter_pairs[signatures.index(s)][overlap_notes_per_slice:])
          sig = signatures[signatures.index(s)]
          total_notes += len(song[-1])
          print('Found', c, 'slices /', total_notes, 'notes...')
          c += 1
          break
    
    if c == i + 1:
      print('=' * 70)
      print('Generator exhausted. Stopping...')
      break
  
  except KeyboardInterrupt:
    print('=' * 70)
    print('Keyboard interrupt requested...')
    print('Saving progress and writing resulting MIDI...')
    break

print('=' * 70)

if c >= i + 1:

  print('Finalizing resulting song...')
  print('=' * 70)
  song1 = []
  for s in song:
    song1.extend(s)
  song1 = [s for s in song1 if type(s) == list]

  print('Analyzing generated song...')
  ptime = 0
  count = 1
  ptime = song1[0][1]
  for s in song1:
    if abs(s[1] - ptime) > 1000:
      count += 1
    ptime = s[1]
  print('Song has', count, 'unique pieces.')
  if count < 2:
    print('PLAGIARIZM WARNING: Your composition is most likely plagiarizm')
  print('=' * 70)

  print('Adding unique pieces labels to the song...')
  song2 = []
  ptime = song1[0][1]
  song2.append(['text_event', song1[0][1], str(song1[0])])
  for s in song1:
    if abs(s[1] - ptime) > 1000:
      song2.append(['text_event', s[1], str(s)])
      song2.append(s)
    else:
      song2.append(s)
    ptime = s[1]
  print('=' * 70)

  print('Recalculating songs timings...')
  song3 = TMIDI.Tegridy_Timings_Converter(song2)[0]
  print('=' * 70)

  print('Total song length:', len(song3))
  print('=' * 70)

  comp_numb = sum([y[4] for y in song3 if y[0] == 'note'])
  comp_length = len(song3)
  print('Endless Piano Composition #:', comp_numb, '-', comp_length)
  print('=' * 70)

  stats = TMIDI.Tegridy_SONG_to_MIDI_Converter(song3,
                                              output_signature='Endless Piano',
                                              output_file_name='/content/Endless-Piano-Music-Composition', 
                                              list_of_MIDI_patches=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
                                              track_name='Composition #:' + str(comp_numb) + '-' + str(comp_length))
  print('=' * 70)

"""# Plot and Listen"""

#@title Install prerequisites
!apt install fluidsynth #Pip does not work for some reason. Only apt works
!pip install midi2audio
!pip install pretty_midi

#@title Plot and listen to the last generated composition
#@markdown NOTE: May be very slow with the long compositions
from midi2audio import FluidSynth
from IPython.display import display, Javascript, HTML, Audio
import pretty_midi
import librosa.display
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

print('Synthesizing the last output MIDI. Please stand-by... ')
fname = '/content/Endless-Piano-Music-Composition'

fn = os.path.basename(fname + '.mid')
fn1 = fn.split('.')[0]
print('Playing and plotting composition...')

pm = pretty_midi.PrettyMIDI(fname + '.mid')

# Retrieve piano roll of the MIDI file
piano_roll = pm.get_piano_roll()

plt.figure(figsize=(14, 5))
librosa.display.specshow(piano_roll, x_axis='time', y_axis='cqt_note', fmin=1, hop_length=160, sr=16000, cmap=plt.cm.hot)
plt.title('Composition: ' + fn1)

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
Audio(str(fname + '.wav'), rate=16000)

"""# Congrats! You did it! :)"""