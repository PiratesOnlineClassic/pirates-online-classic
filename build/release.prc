# Release settings for the compiled client.
#
# nuitka_build.py compiles this file into the client as config/dev.prc.
# PiratesStart always loads config/general.prc, config/dev.prc and
# config/performance.prc (later files win), then config/personal.prc if a
# player made one.  In a release the dev.prc slot holds these release
# settings instead of the developer ones, so the game code stays unchanged.
#
# Not shipped: config/dev.prc (developer settings), config/server.prc (server
# only, and it holds secrets) and config/release/dist_prod.prc (out of date:
# server-port 7198 and server-version poc-alpha-1.0.0 do not match the
# current astron config, and it turns on teleport-all,
# ignore-teleport-requirements and disable-blockers).

# Development: off.
want-dev #f
want-dev-access #f
want-dev-hotkeys #f
want-avatar-physics-indicator #f
visualize-cartesian-grid #f
instant-skill-recharge #f
always-allow-digging #f
always-allow-searching #f
dev-analyics #f
# Typing ">python" in chat runs it in the client (general.prc turns it on).
exec-chat #f

# Resources: the release keeps them in ../resources beside the game folder
# (this file is game/config/dev.prc, so that is ../../resources from here).
# Some game code also reads ../resources/phase_N/etc relative to the working
# directory, which the launcher sets to the game folder.
model-path $THIS_PRC_DIR/../../resources
model-path $THIS_PRC_DIR/../../resources/phase_2
model-path $THIS_PRC_DIR/../../resources/phase_3
model-path $THIS_PRC_DIR/../../resources/phase_4
model-path $THIS_PRC_DIR/../../resources/phase_5

# Caches (performance.prc turns on state-cache and transform-cache).
want-cache #f
want-disk-cache #f
model-cache-textures #f
cache-quest-step #t

# Npc:
want-townfolk #t
want-enemies #t
want-animals #t
want-random-bosses #f

# Tutorial and quests: normal play, no dev skips.
skip-tutorial #f
force-tutorial #f
force-tutorial-complete #f
disable-blockers #f

# Water:
want-low-end-water #f
want-water-panel #f

# Shards:
show-total-population #t
teleport-all #f
shard-page-disable #f
