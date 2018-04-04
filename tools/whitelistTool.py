import os

from pirates.chat import WhiteListData


def acceptWord():
    word = raw_input('> ').rstrip().lower()

    if word == 'save()':
        saveChanges()
        return

    if word.startswith('r '):
        word = word.replace('r ', '')
        if word not in wordslist:
            print 'Could not remove unknown word "%s" from the whitelist.' % word
        else:
            wordslist.remove(word)
            print 'Removed "%s" from the whitelist.' % word
    elif word in wordslist:
        print 'The word "%s" is already whitelisted.' % word
    else:
        wordslist.append(word)
        print 'Added the word "%s" to the whitelist.' % word

    acceptWord()


def saveChanges():
    print 'Saving the whitelist...'

    with open('pirates/chat/WhiteListData.py', 'w') as f:
        f.write('WHITELIST = [\n')

        wordslist.sort()
        addedWords = []

        for word in wordslist:
            if word in addedWords:
                continue
            addedWords.append(word)

            if "'" in word:
                f.write('    "%s",\n' % word)
            else:
                f.write("    '%s',\n" % word)

        f.write(']')

    print 'Saved'


wordslist = WhiteListData.WHITELIST

print 'To add a word, type the word.'
print 'To remove a word, type "r <word>".'
print 'To save exit, type save()".'


acceptWord()