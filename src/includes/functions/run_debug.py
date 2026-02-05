
pre  = ~Filter(SYSRT_CLOCK) >> Print('input', portnames='in') 
post = Print('output',portnames='out')

run(
    control=control_patch,
    scenes=_scenes,
    pre=pre,
    post=post,
)