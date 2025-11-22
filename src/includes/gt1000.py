
#
# The Boss GT-1000 definition file for mididings
# This device has 4 banks, each bank contains 50 programs 
#

gt1k_port = "mpk_midi"

# Internal Midi channel configured in the gt1k USB options
gt1k_channel = 9

gt1kBankSelector = CtrlValueFilter(0, 4) >> [
      Ctrl(gt1k_port, gt1k_channel, EVENT_CTRL, EVENT_VALUE), 
      Ctrl(gt1k_port, gt1k_channel, 32, 0),
]
gt1kBank1 = Ctrl(0, 0) >> gt1kBankSelector
gt1kBank2 = Ctrl(0, 1) >> gt1kBankSelector
gt1kBank3 = Ctrl(0, 2) >> gt1kBankSelector
gt1kBank4 = Ctrl(0, 3) >> gt1kBankSelector

gt1kProgramSelector = Program(gt1k_port, channel = gt1k_channel, program = EVENT_VALUE)
