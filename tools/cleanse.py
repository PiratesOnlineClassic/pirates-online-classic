#!/usr/bin/env python2
import os

for root, _, filenames in os.walk('../'):
    for filename in filenames:
        if filename.endswith('.pyc'):
            filepath = os.path.join(root, filename)
            print 'Deleting %s...' % filepath
            os.unlink(filepath)
