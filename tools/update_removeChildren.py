import os, glob

def scandirs(path):
	for currentFile in glob.glob( os.path.join(path, '*') ):
		if os.path.isdir(currentFile):
			scandirs(currentFile)
		if currentFile.endswith('py'):
			filedata = None
			with open(currentFile, 'r') as file:
				filedata = file.read()

			if not '.removeChildren()' in filedata:
				continue

			filedata = filedata.replace('.removeChildren()', '.get_children().detach()')

			with open(currentFile, 'w') as file:
				file.write(filedata)
			print 'Updated: %s!' % currentFile


if __name__ == '__main__':
	path = '../pirates'
	scandirs(path)
	path = '../otp'
	scandirs(path)
	print 'Done!'