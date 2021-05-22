# -*- coding: utf-8 -*-
"""Endless_Piano.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mkC406W4uAuMgWcklO20WKtHDe4Eg0iU

# Endless Piano (ver. 3.0)

***

## Endless Melody-Conditioned Semi-Generative Performance Piano Music Maker

***

### Powered by tegridy-tools TMIDI and FuzzyWuzzy

***

#### Project Los Angeles

#### Tegridy Code 2021

***

# Setup environment
"""

#@title Install tegridy-tools and FuzzyWuzzy
!git clone https://github.com/asigalov61/tegridy-tools
!pip install fuzzywuzzy[speedup]

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

from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from tqdm import auto

import tqdm
from tqdm import auto

os.chdir('/content/')
print('Loading complete. Enjoy! :)')

"""# Download and load Endless Piano Model (Recommended)

## NOTE: Choose only one
"""

#@title Download large model (GiantMIDI Dataset / Recommended)
# %cd /content/
!wget --no-check-certificate -O Endless-Piano-Music-Model.zip "https://onedrive.live.com/download?cid=8A0D502FC99C608F&resid=8A0D502FC99C608F%2118490&authkey=AEYNr3KP91pq5YI"
!unzip -j Endless-Piano-Music-Model.zip

#@title Download small model (POP909/POP17k Datasets)
!wget https://github.com/asigalov61/Endless-Piano/raw/main/Model/Endless-Piano-Music-Model.zip
!unzip -j Endless-Piano-Music-Model.zip

#@title Load the model
chords_list_f = TMIDI.Tegridy_Any_Pickle_File_Loader('/content/Endless-Piano-Music-Model')

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
miliseconds_per_slice = 1000 #@param {type:"slider", min:1000, max:8000, step:1000}

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
    chords_list_f.append(TMIDI.Tegridy_Score_Slicer(chords, miliseconds_per_slice)[0])

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

# Writing dataset to pickle file
print('Writing dataset to pickle file...')
TMIDI.Tegridy_Pickle_File_Writer(MusicDataset, file_name_to_output_dataset_to)

"""# Generate Music"""

#@title Generate endless Piano performance music
randomize_dataset = False #@param {type:"boolean"}
self_conditioned_generation = False #@param {type:"boolean"}
full_path_to_custom_MIDI_file = "" #@param {type:"string"}
desired_number_of_notes = 500 #@param {type:"slider", min:50, max:1000, step:100}
desired_maximum_fuzzy_match_percentage = 101 #@param {type:"slider", min:1, max:101, step:1}
desired_minimum_fuzzy_match_percentage = 90 #@param {type:"slider", min:0, max:100, step:1}

print('=' * 50)
print('Endless Piano')
print('=' * 50)

print('Prepping data...')
chords_list = []

for c in chords_list_f:
  for cc in c:
    chords_list.append(cc)
    
print('=' * 50)

if randomize_dataset:
  print('Randomizing for freshness... :)')
  random.shuffle(chords_list)
  print('=' * 50)

if full_path_to_custom_MIDI_file != '':
  print('Loading custom MIDI...')
  print(full_path_to_custom_MIDI_file)
  print('=' * 50)

else:
  print('Using randomly selected melody from the dataset')
  print('=' * 50)

print('Generating...')

song = copy.deepcopy(chords_list[secrets.randbelow(len(chords_list))])
if full_path_to_custom_MIDI_file != '':
    t, m, c = TMIDI.Optimus_MIDI_TXT_Processor(full_path_to_custom_MIDI_file, MIDI_patch=range(127), MIDI_channel=-1)
  
else:
  m = chords_list_f[secrets.randbelow(len(chords_list_f))][0]

bre = False

for i in range(len(chords_list)):
  if song == []: l = len(song) * -1
  
  song.extend(chords_list[secrets.randbelow(len(chords_list))])
  
  for i in range(0, len(m)-3, 3):
    for c in chords_list:
      
      try:
        if not self_conditioned_generation:
         if len(c) > 2:
          if fuzz.ratio([c[0][5]], [m[i][5]]) > desired_minimum_fuzzy_match_percentage:

            if fuzz.ratio(c[0][1:], m[i][1:]) > desired_minimum_fuzzy_match_percentage and fuzz.ratio(c[0][1:], m[i][1:]) < desired_maximum_fuzzy_match_percentage:
              if fuzz.ratio(c[1][1:], m[i+1][1:]) > desired_minimum_fuzzy_match_percentage and fuzz.ratio(c[0][1:], m[i+1][1:]) < desired_maximum_fuzzy_match_percentage:
                if fuzz.ratio(c[2][1:], m[i+2][1:]) > desired_minimum_fuzzy_match_percentage and fuzz.ratio(c[0][1:], m[i+2][1:]) < desired_maximum_fuzzy_match_percentage:
                  score = []
                  for cc in c:
                    score.extend(c)
                  song.extend(TMIDI.Tegridy_Timings_Converter(score, 
                                                              fixed_start_time=100, 
                                                              max_delta_time=100,
                                                              mult = secrets.choice([0.1, 0.2, 0.3, 0.9]),
                                                              start_time_multiplier=mult,
                                                              durations_multiplier=mult)[0])
                  
                  if secrets.randbelow(5) == 0: print('Generated:' , len(song), 'notes')
                  if len(song) > desired_number_of_notes: break
                  
                  break
              
        else:
          if fuzz.ratio([y[4] for y in c], [y[4] for y in song[-len(c):]]) > desired_minimum_fuzzy_match_percentage and fuzz.ratio([y[4] for y in c], [y[4] for y in song[-len(c):]]) < desired_maximum_fuzzy_match_percentage:
            if fuzz.ratio([y[2] for y in c], [y[2] for y in song[-len(c):]]) > desired_minimum_fuzzy_match_percentage and fuzz.ratio([y[2] for y in c], [y[2] for y in song[-len(c):]]) < desired_maximum_fuzzy_match_percentage:
              if fuzz.ratio([y[5] for y in c], [y[5] for y in song[-len(c):]]) > desired_minimum_fuzzy_match_percentage and fuzz.ratio([y[5] for y in c], [y[5] for y in song[-len(c):]]) < desired_maximum_fuzzy_match_percentage:
                score = []
                for cc in c:
                  score.extend(c)
                song.extend(TMIDI.Tegridy_Timings_Converter(score, 
                                                            fixed_start_time=100, 
                                                            max_delta_time=100,
                                                            mult = secrets.choice([0.1, 0.2, 0.3, 0.9]),
                                                            start_time_multiplier=mult,
                                                            durations_multiplier=mult)[0])
                
                if secrets.randbelow(5) == 0: print('Generated:' , len(song), 'notes')
                if len(song) > desired_number_of_notes: break

            break

      except KeyboardInterrupt:
        bre = True
        print('Stopping and saving progress...')
        break
      
      except:
        print('Error...Skipping...')
        continue
    
    if bre == True: break
    if len(song) > desired_number_of_notes: break
  
  if len(song) > desired_number_of_notes: break
  if bre == True: break
        
    
print('Done!')
print('=' * 50)

print('Final notes count:', len(song))
print('=' * 50)

stats = TMIDI.Tegridy_SONG_to_MIDI_Converter(TMIDI.Tegridy_Timings_Converter(song, fixed_start_time=100)[0], output_file_name='/content/Endless-Piano-Music-Composition', list_of_MIDI_patches=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], track_name='Endless Piano Composition',)

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