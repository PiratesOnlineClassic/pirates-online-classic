import glob

def processFile(f,t):
    data = open(f,'rb').read()
    lines = data.replace('\r\n','\n').split('\n')
    lines_found = []
    for i,x in enumerate(lines):
        if t in x:
            lines_found.append(i+1)

    return lines_found

term = raw_input('> ')
for x in glob.glob('../pirates/*/*.py'):
    r = processFile(x,term)
    if r:
        print x,r

raw_input('*****')
