import random

from MarginCell import MarginCell
from pandac.PandaModules import *


class MarginManager(PandaNode):

    def __init__(self):
        PandaNode.__init__(self, 'margins')

        self.cells = set()
        self.visiblePopups = set()

    def addGridCell(self, x, y, left, right, bottom, top):
        pass

    def setCellAvailable(self, cell, available):
        cell = cell.getPythonTag('MarginCell')
        cell.setAvailable(available)
        self.reorganize()

    def addVisiblePopup(self, popup):
        self.visiblePopups.add(popup)
        self.reorganize()

    def removeVisiblePopup(self, popup):
        if popup not in self.visiblePopups:
            return
        self.visiblePopups.remove(popup)
        self.reorganize()

    def reorganize(self):
        # First, get all active cells:
        activeCells = [cell for cell in self.cells if cell.isAvailable()]

        # Next, get all visible popups, sorted by priority:
        popups = list(self.visiblePopups)
        popups.sort(key=lambda x: -x.getPriority())

        # We can only display so many popups, so truncate to the number of active
        # margin cells:
        popups = popups[:len(activeCells)]

        # Now, we need to build up a list of free cells:
        freeCells = []
        for cell in activeCells:
            if not cell.hasContent():
                freeCells.append(cell)
            elif cell.getContent() in popups:
                # It's already displaying something we want to show, so we can
                # safely ignore this cell/popup pair:
                popups.remove(cell.getContent())
            else:
                # It's not displaying something we want to see, evict the old
                # popup:
                cell.setContent(None)
                freeCells.append(cell)

        # At this point, there should be enough cells to show the popups:
        assert len(freeCells) >= len(popups)

        # Now we assign the popups:
        for popup in popups:
            if popup._lastCell in freeCells and popup._lastCell.isFree():
                # The last cell it had assigned is available, so let's assign it
                # again:
                popup._lastCell.setContent(popup)
                freeCells.remove(popup._lastCell)
            else:
                # We assign a cell at random.
                cell = random.choice(freeCells)
                cell.setContent(popup)
                freeCells.remove(cell)
