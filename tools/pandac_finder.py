import os, glob

def scandirs(path):
	for currentFile in glob.glob( os.path.join(path, '*') ):
		if os.path.isdir(currentFile):
			scandirs(currentFile)
		if currentFile.endswith('py'):
			filedata = None
			with open(currentFile, 'r') as file:
				filedata = file.read()

			if 'pandac' in filedata:
				print '%s has pandac imports!' % currentFile


if __name__ == '__main__':
	path = '../pirates'
	scandirs(path)
	path = '../otp'
	scandirs(path)
	print 'Done!'