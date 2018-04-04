# Window:
window-title Pirates Online Classic
win-orig -2 -2
win-size 800 600

# Audio:
audio-library-name p3fmod_audio

# Models:
model-path ../resources
model-path ../resources/phase_2
model-path ../resources/phase_3
model-path ../resources/phase_4
model-path ../resources/phase_5
default-model-extension .bam

# DClass:
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Server:
game-server 127.0.0.1
server-version pirates-dev

# Notifier:
notify-level-tiff error
notify-level-dxgsg warning
notify-level-gobj warning
notify-level-loader warning
notify-level-chan fatal
notify-level-pgraph error
notify-level-collide error
notify-level-abs error
notify-level-Actor error
notify-level-DisplayOptions debug
notify-timestamp 1

# Buffer:
framebuffer-alpha 1
framebuffer-multisample #t
multisamples 2
prefer-parasite-buffer 1
force-parasite-buffer 1
alpha-bits 8

# Tutorial:
skip-tutorial #f
