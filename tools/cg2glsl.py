import subprocess
import sys
import os

glsl_extensions = {'v': '.vert', 'f': '.frag', 'g': '.geom'}

if len(sys.argv) != 2:
    print("Usage: cg2glsl.py something.sha")
    sys.exit(1)

fn = sys.argv[1]
if not os.path.isfile(fn):
    print("Failed to find %s" % fn)
    sys.exit(1)

def convert_shader(fn, stage, entry, version=120):
    assert stage in 'vfg'
    profile = 'glsl' + stage
    outfn = os.path.splitext(fn)[0] + glsl_extensions[stage]
    outfile = open(outfn, 'w')

    p = subprocess.Popen(['cgc', '-profile', profile, '-entry', entry, '-po', 'version=%d' % version, fn], stdout=subprocess.PIPE)
    out, err = p.communicate()

    if p.returncode != 0:
        print("cgc returned error code %d" % (p.returncode))
        sys.exit(p.returncode)

    substitutions = [("cg_Vertex", "p3d_Vertex")]
    #if version > 120:
    #    substitutions.append(("shadow2DProj(", "textureProj("))
    #    substitutions.append(("shadow2D(", "texture("))

    outfile.write("// output processed by: %s\n" % (' '.join(sys.argv)))

    lines = out.splitlines()
    if not lines[0].startswith('//'):
        lines = lines[1:]

    for line in lines:
        if line.startswith('//'):
            outfile.write(line + '\n')

            if not line.startswith('//var '):
                continue

            parts = line.split(':')
            _, type, name = parts[0].strip().split()
            binding = parts[1].strip()
            mangled = parts[2].strip()

            if ' ' in mangled:
                mangled = mangled.split(' ', 1)[0]

            if '[' in mangled:
                mangled = mangled.split('[', 1)[0]

            glsl_name = name
            prefix, arg = name.split('_', 1)
            if binding.startswith('$vout.'):
                # Don't touch.
                continue

            elif stage == 'v' and binding.startswith('$vin.') and prefix == "vtx":
                if arg == "position":
                    glsl_name = "p3d_Vertex"
                elif arg.startswith("texcoord") and len(arg) == 9:
                    glsl_name = "p3d_MultiTexCoord" + arg[8]
                else:
                    glsl_name = arg

            elif stage != 'v' and binding.startswith('$vin.'):
                # Don't touch.
                continue

            elif prefix == "k":
                glsl_name = arg

            elif prefix == "tex":
                glsl_name = "p3d_Texture" + arg

            elif prefix == "texpad" or prefix == "texpix":
                sys.stderr.write("WARNING: texpad and texpix inputs are not supported\n")

            elif prefix == "attr":
                if arg == "color":
                    glsl_name = "p3d_Color"
                elif arg == "colorscale":
                    glsl_name = "p3d_ColorScale"
                else:
                    sys.stderr.write("WARNING: %s input is not supported\n" % (name))

            elif prefix == "sys":
                if arg == "time":
                    glsl_name = "osg_FrameTime"
                else:
                    sys.stderr.write("WARNING: %s input is not supported\n" % (name))

            elif prefix in ("alight", "dlight", "plight", "slight", "satten", "texmat", "plane", "clipplane"):
                sys.stderr.write("WARNING: %s inputs are not supported\n" % (prefix))

            if type.endswith('SHADOW'):
                # cgc is buggy
                substitutions.append(("sampler2D " + mangled, "sampler2DShadow " + glsl_name))

            substitutions.append((mangled, glsl_name))
            outfile.write("//\--replaced with %s\n" % glsl_name)

        else:
            for key, value in substitutions:
                line = line.replace(key, value)
            outfile.write(line + '\n')

    print("Successfully wrote %s" % outfn)

code = open(fn, 'r').read()

for stage in 'vfg':
    entry = stage + 'shader'
    if entry in code:
        convert_shader(fn, stage, entry)
