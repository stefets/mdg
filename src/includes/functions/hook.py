
#
# Hook section
#

hook(
    AutoRestart(),
    OSCInterface(),
    MemorizeScene("/tmp/hook.memorize-scene")
)