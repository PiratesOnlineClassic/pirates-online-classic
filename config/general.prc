# Window:
window-title Pirates Online Classic
icon-filename phase_3/etc/Pirates_Adds.ico
win-orig -2 -2
win-size 800 600

# Audio:
audio-library-name p3fmod_audio
audio-output-rate 44100
audio-preload-threshold 1024
audio-music-active #t

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

# Stencil:
stencil-bits 8

# DClass:
dc-file astron/dclass/pirates.dc
dc-file astron/dclass/otp.dc

# Server:
server-port 7198
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
framebuffer-hardware #t
framebuffer-software #f
framebuffer-alpha 1
framebuffer-multisample #t
multisamples 2
prefer-parasite-buffer #t
force-parasite-buffer #f
alpha-bits 8
hardware-animated-vertices #t
basic-shaders-only #f
driver-compress-textures #t
textures-auto-power-2 #t

# Performance:
lock-to-one-cpu #f
lock-to-one-core #f

# Animations:
anim-blend-type normalized_linear
interpolate-frames #t

# Tutorial:
skip-tutorial #f
force-tutorial #f

# Seapatch:
want-seapatch #t

# Special Effects:
want-special-effects #t

# Make A Pirate:
want-make-a-pirate #t
want-new-avatars #t

# Membership:
want-membership #f

# Islands:
want-island-barriers #t
object-load-delay #f

# Motion:
motionfsm-lag #f

# Smoothing:
smooth-lag 0.2
smooth-prediction-lag 0.2

# Analytics:
analytics-game-key 5de6a7ce0decbe613cf1cd172b319faf
analytics-secret-key eb6753270d979378bb301d4b82f27a36d1bcc3bb
want-analytics #t

# Discord:
discord-client-id 442413702428229632
discord-rpc-version 1
want-discord-rich-presence #t
discord-want-elapsed #t
discord-development-message #f
allow-teleport-from-discord #f