
#
# Sonarwalk Generic Control Surface definition -----------------------------------------------
#

# Setup controllers
sonar_rew  = 115
sonar_fwd  = 116
sonar_stop = 117
sonar_play = 118
sonar_rec  = 119

# Allowed controllers
ctrls = [sonar_rec, sonar_stop, sonar_play, sonar_rec, sonar_fwd]
SonarTransportFilter = CtrlFilter(ctrls)    # Use in the control patch

# Trigger value
sonar_trigger_value = 127

# Listen channel
sonar_channel = 1

# Output port
sonar_port = um2_midi_2

# ---------------

# Execution patches
SonarController = Ctrl(sonar_port, sonar_channel, EVENT_CTRL, sonar_trigger_value) 

# Direct DAW patch
SonarStop   = Ctrl(sonar_stop, EVENT_VALUE) >> SonarController
SonarPlay   = [SonarStop, Ctrl(sonar_play, EVENT_VALUE)] >> SonarController
SonarRecord = Ctrl(sonar_rec,  EVENT_VALUE) >> SonarController

# WIP
SonarRewind = Ctrl(sonar_rew, EVENT_VALUE) >> SonarController
SonarForward= Ctrl(sonar_fwd, EVENT_VALUE) >> SonarController

