from pirates.piratesbase import PiratesGlobals

def teamStatus(team1, team2):
    if team1 == team2:
        return PiratesGlobals.FRIEND
    elif team1 in PiratesGlobals.FriendlyTeams and team2 in PiratesGlobals.FriendlyTeams:
        return PiratesGlobals.FRIEND
    elif team1 in PiratesGlobals.NeutralTeams and team2 in PiratesGlobals.NeutralTeams:
        return PiratesGlobals.NEUTRAL
    else:
        return PiratesGlobals.ENEMY

def friendOrFoe(thing1, thing2):
    try:
        if thing1.getPVPTeam() and thing2.getPVPTeam():
            if thing1.getPVPTeam() != thing2.getPVPTeam():
                return PiratesGlobals.PVP_ENEMY
            else:
                return PiratesGlobals.PVP_FRIEND
    except AttributeError:
        pass

    try:
        if thing1.getSiegeTeam() and thing2.getSiegeTeam():
            if thing1.getSiegeTeam() != thing2.getSiegeTeam():
                return PiratesGlobals.PVP_ENEMY
            else:
                return PiratesGlobals.PVP_FRIEND
    except AttributeError:
        pass

    try:
        if thing1.getTeam() == thing2.getTeam() == PiratesGlobals.PLAYER_TEAM and (thing1.isUndead() or thing2.isUndead()):
            return PiratesGlobals.ENEMY
    except AttributeError:
        pass

    try:
        return teamStatus(thing1.getTeam(), thing2.getTeam())
    except AttributeError:
        pass

    return PiratesGlobals.NEUTRAL

def damageAllowed(thing1, thing2):
    status = friendOrFoe(thing1, thing2)
    if status == PiratesGlobals.NEUTRAL:
        return False
    elif status == PiratesGlobals.PVP_ENEMY or status == PiratesGlobals.ENEMY:
        return True
    elif getBase().config.GetBool('want-friendly-fire', 0):
        return True
    else:
        return False