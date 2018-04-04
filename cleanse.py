import os

for root, folders, files in os.walk('.'):
    for filename in files:
        filepath = os.path.join(root, filename)

        if 'cleanse.py' in filepath:
            continue

        if '.git' in filepath:
            continue

        print ("Fixing file: %s..." % filepath)

        f = open(filepath, 'r')
        f_data = f.read()
        f.close()

        if 'base.loadModel' in f_data:
            f_data = f_data.replace('base.loadModel', 'base.loader.loadModel')
        else:
            continue

        f = open(filepath, 'w')
        f.write(f_data)
        f.close()

        print ("Done.")
