# Window:
window-title Pirates Online Classic
icon-filename phase_3/etc/Pirates_Adds.ico
win-orig -2 -2
win-size 800 600

# Audio:
audio-library-name p3fmod_audio
audio-output-rate 44100
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
notify-level-AnimationMixer error
notify-level-UsesAnimationMixer warning
notify-level-DisplayOptions debug
notify-timestamp #t

# Buffer:
framebuffer-hardware #t
framebuffer-software #f
framebuffer-alpha #t
framebuffer-multisample #t
multisamples 2
prefer-parasite-buffer #t
force-parasite-buffer #f
alpha-bits 8
hardware-animated-vertices #t
basic-shaders-only #f
driver-compress-textures #t
textures-auto-power-2 #t
allow-incomplete-render #t

# Performance:
lock-to-one-cpu #f
lock-to-one-core #f
want-disk-cache #t

# Animations:
want-smooth-anims #t
anim-blend-type normalized_linear
interpolate-frames #t

# Options:
enable-frame-rate-counter #t

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
want-avatar-shadows #t
want-new-avatar #t

# Membership:
want-membership #f

# Islands:
want-island-barriers #t
object-load-delay #f

# Motion:
motionfsm-lag #f
avatar-physics-freq 2.0

# Smoothing:
smooth-lag #t
smooth-prediction-lag #t

# Analytics:
analytics-game-key 5de6a7ce0decbe613cf1cd172b319faf
analytics-secret-key eb6753270d979378bb301d4b82f27a36d1bcc3bb
want-analytics #t

# Discord:
discord-client-id 442413702428229632
discord-rpc-version #t
want-discord-rich-presence #t
discord-want-elapsed #t
discord-development-message #f
allow-teleport-from-discord #f

# Text:
want-render2dp #t
text-encoding utf8
direct-wtext #f
text-never-break-before ,.-:?!;
textures-power-2 down

# Clock:
async-request-timeout 80.0
async-request-break-on-timeout #f
clock-mode limited
clock-frame-rate 120
paranoid-clock #t
ime-aware #t
ime-hide #t

# TCP/SSL:
collect-tcp #t
collect-tcp-interval #f.1
verify-ssl #f

# LOD:
default-lod-type fade
lod-fade-time 2
make-grid-lod #t
verify-lods #f

# Texture:
dx-management #f
dx-texture-management #f
retransform-sprites #t
preload-textures #f

# Display:
load-display pandagl
aux-display pandadx9
aux-display pandadx8
aux-display pandagl

# Cache:
model-cache-max-kbytes 262144
launcher-decompress-buffer-size 65536

# Pvp:
want-privateering #t
want-infamy #f

# Other:
test-saint-patricks-day #f
test-fourth-of-july #f
want-enviro-dr #f
want-tattoos #t
want-jewelry #t
want-emotes #t
want-slash-commands #t
want-map-flavor-anims #t
low-weapons-only #t
want-running #f
want-game-options-hdr #f
enforce-clean-exit #t
want-ships #t
game-phase #t
