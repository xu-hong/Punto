# WIP
# 
# time.sleep() is blocking. We will probably need two parts:
# 1. the main part, which is for accepting and handling the inputs, and turning 
# them into sequences
# 2. the actual "sequencing" part, that is the play the notes.
# Those will be be in different threads / processes.
# 
# Dependencies: pygame mingus fluidsynth (optional, with homebrew)
# 
# Two ways to generate sound: 
# Fluidsynth (which takes care of MIDI port itself)
# or, set MIDI output port and connect it to a synth 
# (e.g. Helm or an external one)



import time

import pygame
import pygame.midi
from pygame.locals import *
from mingus.core import notes, chords
from mingus.containers import *
from mingus.midi import fluidsynth

SF2_PATH = "/users/hongxu/Dev/GU/GeneralUser.sf2"

def print_device_info():
    pygame.midi.init()
    _print_device_info()
    pygame.midi.quit()

def _print_device_info():
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))

if __name__ == '__main__':

    # first start fluidsynth
    # like this > fluidsynth /usr/local/Cellar/fluid-synth/2.2.2/share/soundfonts/MuseScore_General.sf3

    pygame.midi.init()
    GRAND_PIANO = 0
    CHURCH_ORGAN = 19
    instrument = CHURCH_ORGAN

    _print_device_info()
    # pick the port we want, e.g. FluidSynth virtual port
    # port = pygame.midi.get_default_output_id()
    # print(f"Using default port {port}")

    port = 6
    midi_out = pygame.midi.Output(port, 0)
    midi_out.set_instrument(instrument)

    
    

    CM = [74, 78, 81]
    D = [74, 76, 81]
    DRUM = [35, 36, 37] * 16
    FM = [72, 76, 79]
    MAX = 127
    CPS = 120
    brief = 60.0/CPS # length of a cycle
    channel = 9
    
    note = DRUM
    volume = MAX # volume is velocity, controlling the loudness
    for n in note:
        midi_out.note_on(n, volume, channel=channel) # 74 is middle C, 127 is "how loud" - max is 127
        time.sleep(brief)

        midi_out.note_off(n, volume, channel=channel)
 
    pygame.midi.quit()
