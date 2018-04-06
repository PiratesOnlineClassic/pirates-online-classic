# Window:
window-title Pirates Online Classic
icon-filename phase_3/etc/Pirates_Adds.ico
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

# Exclude:
exclude-texture-scale BardiT*
exclude-texture-scale BriosoPro*
exclude-texture-scale Buccaneer_outline_1*
exclude-texture-scale playingcards*
exclude-texture-scale gui_*
exclude-texture-scale loading_screen*
exclude-texture-scale loadingscreen_*
exclude-texture-scale loading_window_texture*
exclude-texture-scale vr_*
exclude-texture-scale general_frame_*
exclude-texture-scale drop-shadow

# Culling:
cull-bin gui-popup 60 unsorted
cull-bin shadow 15 fixed
cull-bin ground 14 fixed
cull-bin sky 28 fixed
cull-bin water 28 fixed
cull-bin gui-fixed 55 fixed

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
hardware-animated-vertices #t
basic-shaders-only #f

# GC:
garbage-collect-states #f

# Tutorial:
skip-tutorial #f
force-tutorial #f

# Seapatch:
want-seapatch #t

# Special Effects:
want-special-effects #t

# Make A Pirate:
want-make-a-pirate #t

# Membership:
want-membership #f

# Islands:
remove-island-barriers #f
object-load-delay #f
