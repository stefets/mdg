#!/bin/bash

# Ensure that no other instances of mpv are running
pkill mpv

# Remove any existing socket files and log files
rm -f \
    /tmp/sd90-a.sock \
    /tmp/sd90-b.sock \
    /tmp/sd90-video.sock \
    /tmp/u192k-a.sock \
    /tmp/u192k-b.sock \
    /tmp/u192k-video.sock \
    /tmp/video.sock
rm -f \
    /tmp/mpv-sd90-a.log \
    /tmp/mpv-sd90-b.log \
    /tmp/mpv-u192k-a.log \
    /tmp/mpv-u192k-b.log \
    /tmp/mpv-u192k-video.log \
    /tmp/mpv-sd90-video.log \
    /tmp/mpv-video.log

# Start mpv instances for each audio device with the specified options

# ---------------------------------- SD90 ----------------------------------
# Audio only on device: SD90 (Socket: /tmp/sd90-a.sock)
mpv --idle=yes --keep-open=no --no-video --no-terminal \
    --input-ipc-server=/tmp/sd90-a.sock --audio-device=alsa/SD90 \
    --log-file=/tmp/mpv-sd90-a.log --msg-level=all=info  &

# Audio only on device: SD90 (Socket: /tmp/sd90-b.sock)
mpv --idle=yes --keep-open=no --no-video --no-terminal \
    --input-ipc-server=/tmp/sd90-b.sock --audio-device=alsa/SD90 \
    --log-file=/tmp/mpv-sd90-b.log --msg-level=all=info  &

# Video and audio on device: SD90 (Socket: /tmp/sd90-video.sock)
mpv --idle=yes --keep-open=no --no-terminal \
    --input-ipc-server=/tmp/sd90-video.sock --audio-device=alsa/SD90 \
    --log-file=/tmp/mpv-sd90-video.log --msg-level=all=info  &

# ---------------------------------- U192k ----------------------------------
# Audio only on device: U192k (Socket: /tmp/u192k-a.sock)
mpv --idle=yes --keep-open=no --no-video --no-terminal \
    --input-ipc-server=/tmp/u192k-a.sock --audio-device=alsa/U192k \
    --log-file=/tmp/mpv-u192k-a.log --msg-level=all=info &

# Audio only on device: U192k (Socket: /tmp/u192k-b.sock)
mpv --idle=yes --keep-open=no --no-video --no-terminal \
    --input-ipc-server=/tmp/u192k-b.sock --audio-device=alsa/U192k \
    --log-file=/tmp/mpv-u192k-b.log --msg-level=all=info &

# Video and audio on device: U192k (Socket: /tmp/u192k-video.sock)
mpv --idle=yes --keep-open=no --no-terminal \
    --input-ipc-server=/tmp/u192k-video.sock --audio-device=alsa/U192k \
    --log-file=/tmp/mpv-u192k-video.log --msg-level=all=info &

# ---------------------------------- VIDEO ONLY ----------------------------------
mpv --idle=yes --keep-open=no --no-terminal \
    --input-ipc-server=/tmp/video.sock \
    --ao=null &