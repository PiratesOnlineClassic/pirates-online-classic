# Window:
window-title Pirates Online Classic [ALPHA]
icon-filename Pirates_Adds.ico
win-origin -1 -1
win-size 800 600
fullscreen #f
server-version poc-alpha-1.0.0

# Animations:
want-alt-idles #t
want-zombie #t
want-idle-centered #f
npc-sidestep #f
osd-anim-blends #f
want-splash-anims #t
motionfsm-lag #f
restore-initial-pose #f
want-smooth-anims #t
even-animation #t
interpolate-frames #t
hardware-animated-vertices #t
anim-blend-type normalized_linear

# Water:
want-low-end-water #t

# Lod:
default-lod-type fade
make-grid-lod #t
verify-lods #f

# Graphics
allow-live-flatten #t
framebuffer-hardware #t
framebuffer-software #f
framebuffer-alpha 1
framebuffer-multisample #t
alpha-bits 8
prefer-parasite-buffer #t
force-parasite-buffer #t
retransform-sprites #t
matrix-palette #t

# Stenciles:
stencil-bits 8

# SRGB:
framebuffer-srgb #f

# Holidays:
want-holidays #t

# Text:
text-encoding utf8
direct-wtext #f
text-never-break-before 1
text-flatten 0
text-dynamic-merge 1
text-minfilter linear
text-magfilter linear
text-page-size 512 512
text-rwap-mode WM_border_clor

# Audio
audio-output-rate 44100
audio-library-name p3fmod_audio
audio-music-active #t
low-memory-stream-audio #t

# Quests:
disable-blockers #t

# Cache
want-cache #t
want-disk-cache #f
state-cache #t
transform-cache #t
model-cache-textures #f
cache-quest-step #t

# Chat
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

# Compass/map
want-compass-task #t
map-islands-debug #f
want-momentary-minimap #t

# Effects
want-special-effects #t
want-grass #t
want-shaders #t
want-avatar-shadows #t
want-special-effects #t
want-particles #t
support-threads #t
empty-node-path future

# Performance:
lock-to-one-cpu #f
lock-to-one-core #f

# Animations:
anim-blend-type normalized_linear
interpolate-frames #t

# GL Debug
gl-check-errors #f

# GUI
hide-gui #f

# Island
remove-island-barriers #f

# Make A Pirate
want-jail-lights-off #f
want-new-avatars #t
want-npc-viewer #f
want-marketing-viewer #f
want-jewelry #t
want-gen-pics-buttons #f
want-socks #f
want-map-flavor-anims #t
want-map-coats #f
avchooser-allow-logout #f
disable-server-queueing #t
show-total-population #t

# Tutorial:
skip-tutorial #t
force-tutorial #f
ignore-teleport-requirements #t
force-tutorial-complete #t

# Teleport:
teleport-all #t

# World:
default-world piratesWorld

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
notify-level-AnimationMixer error
notify-level-UsesAnimationMixer warning
notify-level-DisplayOptions debug

# Options:
disable-pirates-options #f
enable-stereo-display #t

# Font:
text-default-font models/fonts/BardiT_outline.bam

# Display:
aux-display pandagl

# Resources:
default-model-extension .bam
model-cache-max-kbytes 262144
preload-textures 1
textures-power-2 down
texture-magfilter linear
texture-minfilter linear
texture-quality-level fastest
driver-compress-textures #t

# Server:
server-port 7198
server-version pirates-dev

# Water
want-water-reflections #t
want-water-reflection-show-through-only #t
want-seapatch #t
want-water-panel #f
flagship-wave-count 2

# Shadows:
want-avatar-shadows #t

# Movement:
smooth-lag 1

# Leaks:
crash-on-proactive-leak-detect #f

# Server Queue:
disable-server-queueing #t

# Textures:
textures-power-2 down
texture-anisotropic-degree 16
texture-magfilter linear
texture-minfilter linear
texture-quality-level fastest
driver-compress-textures #t

# Shaders:
gl-validate-shaders #f
gl-skip-shader-recompilation-warnings #t

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

# Disney Stuff
want-render2dp 1
text-encoding utf8
direct-wtext 0
text-never-break-before 1
ime-aware 1
ime-hide 1
paranoid-clock 1
collect-tcp 1
collect-tcp-interval 0.1
verify-ssl 0
extra-ssl-handshake-time 20.0
audio-output-rate 44100
smooth-lag 1
default-lod-type fade
want-disk-cache 1
lock-to-one-cpu 1
stencil-bits 8
framebuffer-alpha 1
alpha-bits 8
dx-management 0
dx-texture-management 0
prefer-parasite-buffer 1
force-parasite-buffer 1
http-connect-timeout 20
http-timeout 30
want-dev 0
want-new-avatar 1
async-request-timeout 80.0
async-request-break-on-timeout 0
notify-timestamp 1
enforce-clean-exit 1
restore-initial-pose 0
empty-node-path future
crash-on-proactive-leak-detect 0
enable-stereo-display 1
want-background-region 0
allow-async-bind 1
