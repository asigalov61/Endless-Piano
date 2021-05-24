# -*- coding: utf-8 -*-
"""Endless_Piano.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10eDAh121hGrGJQ7RCblTI770WUf59VyB

# Endless Piano (ver. 5.0)

***

## Endless Semi-Generative Performance Piano Music Maker

***

### Powered by tegridy-tools TMIDI

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

from tqdm import auto

import secrets
import random

if not os.path.exists('/content/Dataset'):
    os.makedirs('/content/Dataset')

if not os.path.exists('/content/Output'):
    os.makedirs('/content/Output')

os.chdir('/content/tegridy-tools/tegridy-tools')
import TMIDI

import tqdm
from tqdm import auto

os.chdir('/content/')
print('Loading complete. Enjoy! :)')

"""# Download and load processed GiantMIDI dataset (Required)

## NOTE: Loading will take about 10 minutes and 20GB RAM
"""

#@title Download processed GiantMIDI dataset (Required)
# %cd /content/
!wget --no-check-certificate -O GiantMIDI.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118491&authkey=AKrxNM53z9DGX2Y"
!unzip -j GiantMIDI.zip

#@title Load the dataset

#@markdown NOTE: This may take a while. Please wait...
print('Loading GiantMIDI...')
data = TMIDI.Tegridy_Any_Pickle_File_Loader('/content/GiantMIDI')
print('Randomizing dataset...')
random.shuffle(data[0])
print('Processing data...')
quarter_pairs = []
for d in auto.tqdm(data[0]):
  quarter_pairs.extend(TMIDI.Tegridy_Sliced_Score_Pairs_Generator(d, 250, shuffle_pairs=True)[0])
print('Done! Enjoy!')

"""# (OPTIONAL) Process your own dataset"""

#@title Process MIDIs to special MIDI dataset with Tegridy MIDI Processor

desired_dataset_name = "Endless-Piano-Music-Dataset" #@param {type:"string"}
file_name_to_output_dataset_to = "/content/Endless-Piano-Music-Dataset" #@param {type:"string"}
desired_MIDI_channel_to_process = -1 #@param {type:"slider", min:-1, max:16, step:1}
encode_MIDI_channels = False #@param {type:"boolean"}
encode_velocities = False #@param {type:"boolean"}
chordify_input_MIDIs = False #@param {type:"boolean"}
melody_conditioned_encoding = False #@param {type:"boolean"}
melody_pitch_baseline = 60 #@param {type:"slider", min:1, max:127, step:1}
time_denominator = 1 #@param {type:"slider", min:1, max:20, step:1}
chars_encoding_offset = 196 #@param {type:"number"}
miliseconds_per_slice = 250

print('TMIDI Processor')
print('Starting up...')

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
print('Processing MIDI files. Please wait...')
for f in tqdm.auto.tqdm(filez):
  try:
    fn = os.path.basename(f)

    fnn = fn
    fn1 = fnn.split('.')[0]
    fn3 = ['Unknown']

    #fn2 = fn.split('.')[0]
    #fn3 = lakh[str(fn2)]
    #fn1 = fn3[0].split('.')[-2].split('/')[-1]

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
                                                           perfect_timings=True)
    chords_list_f.append(chords)

    melody_list_f.append(melody)

    pf.append([fn1, f.split('/')[-2], f.replace('/content/Dataset/','/LAKH/clean_midi/')])


    files_count += 1

  except KeyboardInterrupt:
    print('Exiting...Saving progress...')
    break

  except:
    bf += 1
    print('Bad MIDI:', f)
    print('Count:', bf)
    
    continue

#print('Stamping total number of songs...')
#TXT_String += 'TOTAL_SONGS_COUNT=' + str(files_count)

print('Task complete :)')
print('==================================================')
#print('Number of processed dataset MIDI files:', files_count)
#print('Number of MIDI chords recorded:', len(chords_list_f))
#print('First chord event:', chords_list_f[0], 'Last chord event:', chords_list_f[-1]) 
#print('Number of recorded melody events:', len(melody_list_f))
#print('First melody event:', melody_list_f[0], 'Last Melody event:', melody_list_f[-1])
#print('Total number of MIDI events recorded:', len(chords_list_f) + len(melody_list_f))

# Writing dataset to TXT file
#print('Writing dataset to TXT file...')
#with open(file_name_to_output_dataset_to + '.txt', 'wb') as f:
  #f.write(TXT_String.encode('utf-8', 'replace'))
  #f.close

# Dataset
print('Finalizing the dataset...')
MusicDataset = [chords_list_f, melody_list_f, kar_ev, filez, pf, bf, files_count]
print('Randomizing dataset...')
random.shuffle(chords_list_f)
print('Processing data...')
quarter_pairs = []
for d in auto.tqdm(chords_list_f):
  quarter_pairs.extend(TMIDI.Tegridy_Sliced_Score_Pairs_Generator(d, 250, shuffle_pairs=True)[0])
print('Done! Enjoy!')
TMIDI.Tegridy_Pickle_File_Writer(MusicDataset, file_name_to_output_dataset_to)

"""# Generate Music"""

#@title Generate Endless Classical Piano Music

#@markdown NOTE: There is nothing to tune or adjust. The process is fully random and automatic. Just re-run the generator to generate new compositions :)

#@markdown NOTE: If nothing is being generated or if the song is too short: re-run the generator.
number_of_chord_pairs_to_generate = 200 #@param {type:"slider", min:50, max:500, step:50}

song = []
qp_idx = 0
stime = 0
qtime = 0
pairs = []

debug = False

print('=' * 100)
print('Endless Piano')
print('=' * 100)

print('Starting first pair search. This may take some time...')
print('=' * 100)
for i in auto.tqdm(range(len(quarter_pairs))):
  try:
    seed = quarter_pairs[secrets.randbelow(len(quarter_pairs))]

    for q in quarter_pairs:
        
        seed1 = [y[2:] for y in seed[1]]
        q1 = [y[2:] for y in q[0]]
        if seed1 == q1:
              print('Found the first matching pair...')
              print('=' * 100)
              print(seed)
              print(q)
              print('=' * 100)
              qp_idx = quarter_pairs.index(q)

              break

    if qp_idx != 0:
      song.extend(seed[0])
      song.extend(seed[1])
      pairs.append(seed)
      print('Song length so far:', len(song))
      print('=' * 100)
      break
  
  except KeyboardInterrupt:
    break
  
  except:
    pass

#=============Main search loop

print('Starting main pairs search...')
print('Please stand-by...')
print('=' * 100)
song1 = []
spairs = []
for r in auto.tqdm(range(number_of_chord_pairs_to_generate)):
  try:
    song = []
    for i in range(len(quarter_pairs)):

      
        seed = quarter_pairs[qp_idx]
        
        for q in quarter_pairs[:secrets.randbelow(len(quarter_pairs))]:
            
            seed1 = [y[2:] for y in seed[1]]
            q1 = [y[2:] for y in q[0]]
            if seed1 == q1:
                if debug:
                  print('Found the first matching pair...')
                  print('=' * 100)
                  print(seed)
                  print(q)
                  print('=' * 100)
                if seed not in pairs:
                  qp_idx = quarter_pairs.index(q)
                  break               

        if qp_idx != 0:
          song.extend(seed[0])
          song.extend(seed[1])
          pairs.append(seed)
          if secrets.randbelow(50) == 0:
            print('Song length so far:', len(song1))
            print('=' * 100)
          break

    song1.extend(song)
    spairs.extend(pairs)

  except KeyboardInterrupt:
    break
  
  except:
    pass

print('Done!')
print('=' * 100)

print('Total song length:', len(song1))
print('=' * 100)

print('Recalculating songs timings...')
print('=' * 100)
song = TMIDI.Tegridy_Timings_Converter(song1)[0]

print('Writing MIDI')
comp_numb = sum([y[4] for y in song])
comp_length = len(song)
print('Endless Piano Composition #:', comp_numb, '-', comp_length)
print('=' * 100)

stats = TMIDI.Tegridy_SONG_to_MIDI_Converter(song,
                                            output_signature='Endless Piano',
                                            output_file_name='/content/Endless-Piano-Music-Composition', 
                                            list_of_MIDI_patches=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 
                                            track_name='Composition #:' + str(comp_numb) + '-' + str(comp_length))
print('=' * 100)

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
librosa.display.specshow(piano_roll, x_axis='time', y_axis='cqt_note', sr=64000, cmap=plt.cm.hot)
plt.title('Composition: ' + fn1)

FluidSynth("/usr/share/sounds/sf2/FluidR3_GM.sf2", 16000).midi_to_audio(str(fname + '.mid'), str(fname + '.wav'))
Audio(str(fname + '.wav'), rate=16000)

"""# Congrats! You did it! :)"""