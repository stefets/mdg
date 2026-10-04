from typing import Any
from mididings.util import offset
from mididings.engine import output_event
from mididings.event import ProgramEvent, CtrlEvent

target_port = "tonex_midi"  # The output port where the MIDI messages will be sent
target_channel = 13         # The listen channel configured in the ToneX

class ToneX:
    '''A callable object that activate a preset by name.
    Usage : Call(ToneX("00A"))
    Logic:
        Bank 0 (00A-42C) → 0 to 127
        Bank 1 (43A-49C) → 0 to 23
    '''
    def __init__(self, key) -> None:
        self.key = key

    
    def __call__(self, ev) -> Any:
        ''' Send the patch change to the ToneX'''
        bank, program = self.get_by_key(self.key)
        self.set_bank(bank)
        self.set_program(program)
    
    
    def set_bank(self, bank) -> Any:
        '''Send a Bank Change to the ToneX'''
        output_event(CtrlEvent(target_port, target_channel, 0, bank))
    
    
    def set_program(self, program) -> Any:
        '''Send a Program Change to the ToneX'''
        output_event(ProgramEvent(target_port, target_channel, program))

    
    def get_by_key(self, key: str) -> tuple[int, int]:
        '''Extract bank and program numbers from a ToneX patch key'''
        bank = int(key[:2])
        preset = ord(key[2].upper()) - ord('A')

        program = bank * 3 + preset

        if program <= 127:
            return 0, offset(program)

        return 1, offset(program - 128)
