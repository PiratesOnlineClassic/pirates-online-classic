# Window:
window-title Pirates Online Classic
icon-filename phase_3/etc/Pirates_Adds.ico
win-size 800 600
fullscreen #f

# Development:
want-dev #f
gl-check-errors #f
test-saint-patricks-day #f
test-fourth-of-july #f
want-enviro-dr #f

# Display:
load-display pandagl
aux-display pandadx9
aux-display pandadx8
aux-display p3tinydisplay

# Audio:
audio-music-active #t
low-memory-stream-audio #t
audio-library-name p3fmod_audio
audio-output-rate 44100

# Models:
want-disk-cache #f
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
server-port 6667
server-version pirates-dev
want-ssl-scheme 0
want-user-funnel #f

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
notify-level-express error
notify-timestamp 1

# Frame Buffer:
framebuffer-hardware #t
framebuffer-software #f
framebuffer-alpha 1
alpha-bits 8

# Parasite Buffer:
prefer-parasite-buffer 1
force-parasite-buffer 1
retransform-sprites #t

# Chat:
chat-history-size 10
exec-chat #t
want-chat #t
want-chat-history #t
want-emotes 1
want-sliding-chat #t
want-whitelist #f
want-slash-commands #t
white-list-check-before-send #f
whitelist-chat-enabled #f

# Compass/Map:
map-islands-debug #f

# SRGB:
framebuffer-srgb #f

# Animation:
anim-blend-type normalized_linear
hardware-animated-vertices #f

# Performance:
lock-to-one-cpu #f
lock-to-one-core #f

# Tutorial:
skip-tutorial #f
force-tutorial #t
force-tutorial-complete #f

# Water:
want-seapatch #t

# Effects:
want-special-effects #t
want-grass #f
want-shaders #t
want-avatar-shadows #t
want-special-effects #t
want-particles #t
support-threads #t
empty-node-path future

# Membership:
want-membership #t

# Islands:
want-island-barriers #t
object-load-delay #f
remove-island-barriers #f

# Motion:
motionfsm-lag #f
avatar-physics-freq 60.0
npc-sidestep #f

# Smoothing:
smooth-lag 1
smooth-prediction-lag 1

# Discord:
discord-client-id 442413702428229632
discord-rpc-version 1
want-discord-rich-presence #t
discord-want-elapsed #t
discord-development-message #f
allow-teleport-from-discord #f

# Quests:
disable-blockers #f

# Text:
want-render2dp 1
text-encoding utf8
direct-wtext 0
text-never-break-before ,.-:?!;
textures-power-2 down

# Clock:
async-request-timeout 80.0
async-request-break-on-timeout 0
clock-mode limited
clock-frame-rate 120
paranoid-clock 1

# IME:
ime-aware 1
ime-hide 1

# TCP/SSL:
collect-tcp 1
collect-tcp-interval 0.1
verify-ssl 0

# LOD:
default-lod-type fade
lod-fade-time 2
make-grid-lod 1
verify-lods 0

# Texture:
textures-auto-power-2 #t
dx-management 0
dx-texture-management 0
retransform-sprites 1
preload-textures 0
allow-incomplete-render 1

# Misc:
want-tattoos 1
want-jewelry 1
want-emotes 1
want-slash-commands 1
want-magic-words 1
want-map-flavor-anims 1
low-weapons-only 1
want-running 0
enforce-clean-exit 1
want-ships 1
game-phase 1

# Game Options:
want-game-options-hdr 0
want-game-options-ship-visibility 1
want-cpu-frequency-warning #f
disable-pirates-options #f
want-anti-aliasing-opt #f

# Cache:
model-cache-max-kbytes 262144
launcher-decompress-buffer-size 65536

# Pvp:
want-privateering 1
want-infamy 0

# Options:
ocean-visibility #t

# GUI
hide-gui #f

# Make-A-Pirate:
want-new-avatars #t
want-npc-viewer #f
want-marketing-viewer #f
want-jewelry #t
want-gen-pics-buttons #f
want-socks #f
want-map-flavor-anims #t
want-map-coats #f
want-avatar-shadows #t
want-new-avatar #t

# Shards:
show-total-population #t
