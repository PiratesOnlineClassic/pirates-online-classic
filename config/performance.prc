# Debugging:
pstats-gpu-timing #f
gl-debug #f
gl-debug-object-labels #f

# Disable V-Sync
sync-video #f

# Enable state cache, this seems to actually help the performance by a lot
state-cache #t
transform-cache #t

# Set text settings
text-minfilter linear
text-magfilter linear
text-page-size 512 512
text-rwap-mode WM_border_clor

# Better text performance since rdb's patch
text-flatten 0
text-dynamic-merge 1

# For smoother animations
even-animation #t

# Don't rescale textures which are no power-of-2
textures-power-2 none

# Set default texture filters
texture-anisotropic-degree 16
texture-magfilter linear
texture-minfilter linear
texture-quality-level fastest

# Use the default coordinate system, this makes our matrix transformations
# faster because we don't have have to transform them to a different coordinate
# system before
gl-coordinate-system default

# This makes animations smoother, especially if they were exported at 30 FPS
# and are played at 60 FPS
interpolate-frames #t

## Animations on the gpu. The default shader has to get adjusted to support this
## feature before this option can be turned on.
hardware-animated-vertices #t

uniquify-matrix #t
uniquify-transforms #t
uniquify-states #t
uniquify-attribs #f

## Enable garbarge collection
garbage-collect-states #t
garbage-collect-states-rate 0.2

## Compress textures on the drivers?
driver-compress-textures #t

## Faster animations? (Have to test)
matrix-palette #t
display-list-animation #t

## Better GL performance by not using gl-finish and so on
gl-finish #f
gl-force-no-error #t
gl-check-errors #f
gl-force-no-flush #t
gl-force-no-scissor #t

## Eventually disable memory barriers, have to check if this is faster
gl-enable-memory-barriers #f

# Let the driver generate the mipmaps
driver-generate-mipmaps #t

# Use immutable texture storage, it is *supposed* to be faster, but might not be
# XXX: Seems to produce an GL_INVALID_VALUE when disabled
gl-immutable-texture-storage #t

# Small performance gain by specifying fixed vertex attribute locations.
# Might cause issues with some (incorrectly converted/loaded) meshes though
gl-fixed-vertex-attrib-locations #f

# Disable the fragment shader performance warning
gl-validate-shaders #f
gl-skip-shader-recompilation-warnings #t

# Required for correct velocity
always-store-prev-transform #t
allow-incomplete-render #t
no-singular-invert #f