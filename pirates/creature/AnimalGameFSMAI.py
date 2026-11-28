from direct.directnotify.DirectNotifyGlobal import directNotify

from pirates.creature.CreatureGameFSMAI import CreatureGameFSMAI


class AnimalGameFSMAI(CreatureGameFSMAI):
    notify = directNotify.newCategory('AnimalGameFSMAI')

    def defaultFilter(self, request, args):
        # animals are ambient creatures, they cannot be fought and will
        # never enter battle with anyone...
        if request in ['Battle', 'AttackChase', 'BreakCombat']:
            return None

        # animals never lie in wait for an ambush either...
        if request == 'Ambush':
            return ('Idle',) + tuple(args)

        return CreatureGameFSMAI.defaultFilter(self, request, args)
