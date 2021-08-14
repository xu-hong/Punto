# WIP
# 
# time.sleep() is blocking. We will probably need two parts:
# 1. the main part, which is for accepting and handling the inputs, and turning 
# them into sequences
# 2. the actual "sequencing" part, that is the play the notes.
# Those will be be in different threads / processes.
# 
# Dependencies: pygame(?) mingus fluidsynth (with homebrew)



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

    # pygame.midi.init()
    # GRAND_PIANO = 0
    # CHURCH_ORGAN = 19
    # instrument = CHURCH_ORGAN

    # port = pygame.midi.get_default_output_id()
    # print(f"Using default port {port}")
    # midi_out = pygame.midi.Output(port, 0)
    # midi_out.set_instrument(instrument)
    

    # CM = [74, 78, 81]
    # D = [74, 76, 81]
    # DRUM = [35] * 16
    # FM = [72, 76, 79]
    # MAX = 127
    # CPS = 130
    # brief = 60.0/130 # length of a cycle
    
    # note = DRUM
    # volume = MAX # volume is velocity, controlling the loudness
    # for n in note:
    #     midi_out.note_on(n, volume, channel=10) # 74 is middle C, 127 is "how loud" - max is 127
    #     time.sleep(brief)
    #     midi_out.note_off(n, volume, channel=10)
 
    # pygame.midi.quit()


    fluidsynth.init(SF2_PATH)

    n = Note("C-5")
    n.channel = 9
    fluidsynth.set_instrument(9, 42)
    n.velocity = 100
    fluidsynth.play_Note(n)
    time.sleep(1)
    fluidsynth.stop_Note(Note("C-5"))