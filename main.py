import random
from scipy.io.wavfile import write
import numpy as np
from pydub import AudioSegment


samplerate = 44100

octavas = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
acordescomunes=['Ace','ACE','CEG','CdG','DfA','DFA','EgB','EGB','FAC','FgC','GBD','GaD']
frecuencias = {'c0': 16.35, 'c1': 32.7, 'c2': 65.41, 
'c3': 130.81, 'c4': 261.63, 'c5': 523.25, 
'c6': 1046.50, 'c7': 2093.0, 'c8': 4186.1}

progreciones=[
    {
        'C':'CEG-GBD-ACE-FAC',
        'd':'cFA-gCd-aDF-GaD',
        'D':'DfA-AcE-aBF-GBD',
        'E':'EgB-Bdf-cEg-AcE',
        'G':'GBD-DfA-EGB-CEG'
    },
     {
        'C':'CEG-FAC-GBD',
        'D':'DfA-GBD-AcE',
        'E':'EgB-AcE-Bdf',
        'F':'FAC-aDF-CEG',
        'G':'GBD-CEG-DfA',
        'A':'AcE-DfA-EgB',
        'B':'Bdf-EgB-fac'
    }
]
octav = ['C', 'D', 'd', 'E'] 

def get_piano_notes():
    '''
    Returns a dict object for all the piano 
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    acordescomunes=['Ace','ACE','CEG','CéG','DfA','DFA','EgB','EGB','FAC','FáC','GBD','Gb´D']
    numero = random.randint(3, 4)
    
    base_freq = frecuencias['c'+str(numero)] #Frequency of Note C4
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    note_freqs[''] = 0.0
    
    return note_freqs
    
def get_piano_notesnotas():
    '''
    Returns a dict object for all the piano 
    note's frequencies
    '''
    # White keys are in Uppercase and black keys (sharps) are in lowercase
    octave = ['C', 'c', 'D', 'd', 'E', 'F', 'f', 'G', 'g', 'A', 'a', 'B'] 
    base_freq = 349.2/2 #Frequency of Note C4
    
    note_freqs = {octave[i]: base_freq * pow(2,(i/12)) for i in range(len(octave))}        
    note_freqs[''] = 0.0
    
    return note_freqs

def get_wave(freq, duration=4):
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave
    
def get_wavenotas(freq, duration=4):
    amplitude = 4096
    t = np.linspace(0, duration, int(samplerate * duration))
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    
    return wave
    
def get_song_data(music_notes):
    note_freqs = get_piano_notesnotas()
    song = [get_wavenotas(note_freqs[note]) for note in music_notes.split('-')]
    
    song = np.concatenate(song)
    return song.astype(np.int16)
    
def get_chord_data(chords):
    chords = chords.split('-')
    note_freqs = get_piano_notes()
    
    chord_data = []
    for chord in chords:
        data = sum([get_wave(note_freqs[note]) for note in list(chord)])
        chord_data.append(data)
    
    chord_data = np.concatenate(chord_data, axis=0)    
    return chord_data.astype(np.int16)


def main():
    #Notes of "twinkle twinkle little star"
    music_notes = 'C-E-G-G-B-D-a-D-F-F-A-C'
    nota= random.randint(0, 6)
    prog=random.randint(0, 1)
    print(prog)
    progre = progreciones[prog][octav[nota]]
    #progre = progreciones[0]['G']
    chords=progre
    print(progre)
    for a in range(3):
        chords= chords+'-'+chords
        music_notes = music_notes+'-'+music_notes
    #music_notes = 'C-C-G-G-A-A-G--F-F-E-E-D-D-C--G-G-F-F-E-E-D--G-G-F-F-E-E-D--C-C-G-G-A-A-G--F-F-E-E-D-D-C'
    data = get_song_data(music_notes)
    data = data * (16300/np.max(data))
    write('twinkle-twinkle.wav', samplerate, data.astype(np.int16))
    
    data = get_chord_data(chords)
    data = data * (16300/np.max(data))
    data = np.resize(data, (len(data)*5,))
    write('exp-C-Major.wav', samplerate, data.astype(np.int16))

    sound1 = AudioSegment.from_file("twinkle-twinkle.wav")
    sound2 = AudioSegment.from_file("exp-C-Major.wav")

    combined = sound1.overlay(sound2)

    combined.export("combined.wav", format='wav')
    
if __name__=='__main__':
    main()
