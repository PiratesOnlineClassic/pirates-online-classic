import os, glob

def scandirs(path):
	for currentFile in glob.glob( os.path.join(path, '*') ):
		if os.path.isdir(currentFile):
			scandirs(currentFile)
		if currentFile.endswith('rgb'):
			print 'Removing: %s' + currentFile
			os.remove(currentFile)

scandirs('../resources')
print 'Done!'