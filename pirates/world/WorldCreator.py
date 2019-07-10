from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
from direct.showbase import DirectObject
from pirates.world import WorldCreatorBase
from pirates.leveleditor import ObjectList
from pirates.piratesbase import PiratesGlobals
from pirates.leveleditor import EditorGlobals
from pirates.leveleditor import WorldDataGlobals
from pirates.effects import DynamicLight
from direct.actor import Actor
from otp.otpbase import OTPRender
from pirates.world import ClientArea

class WorldCreator(WorldCreatorBase.WorldCreatorBase, DirectObject.DirectObject):
    notify = directNotify.newCategory('WorldCreator')
    animPartsDict = {
        'Crane': [
            ('Hpr', 2, Point3(10, 10, 0), Point3(-10, -10, 0), '')]}
    
    def __init__(self, cr, worldFile, district):
        self.fileDicts = {}
        self.propNum = 0
        self.cr = cr
        self.district = district
        WorldCreatorBase.WorldCreatorBase.__init__(self, cr, worldFile)
        self.portalAreas = []
        self.postLoadCalls = []
        self.oceanAreas = {}

    def destroy(self):
        self.district = None

    def cleanupAllAreas(self):
        self.portalAreas = []

    def loadObjectsFromFile(self, filename, parent, parentUid = None, dynamic = 0, zoneLevel = 0, startTime = None, merge = False):
        if filename in self.fileDicts:
            return self.fileDicts
        
        fileData = self.openFile(filename)
        if parentUid:
            fileDict = {
                'filename': fileData}
            if merge:
                parentUid = fileData['Objects'].keys()[0]
            
            self.loadObjectsByUid(parent, parentUid, dynamic = dynamic, fileDict = fileDict, zoneLevel = zoneLevel, startTime = startTime)
        elif parent == self.district:
            self.loadOceanData(filename, fileData)
        
        self.fileDicts[filename] = fileData
        return self.fileDicts
    
    def loadOceanData(self, filename, fileData):
        oceanAreas = fileData.get(WorldDataGlobals.OCEAN_AREAS)
        if oceanAreas:
            self.oceanAreas[filename] = oceanAreas

    def getOceanData(self, filename):
        return self.oceanAreas.get(filename)
    
    def loadObjectsByUid(self, parent, parentUid, dynamic = 0, fileDict = None, zoneLevel = 0, startTime = None):
        if fileDict == None:
            fileDict = self.fileDicts
        
        objectInfo = self.getObjectDataByUid(parentUid, fileDict)
        if not objectInfo:
            if len(parent.links):
                tunnel = base.cr.doId2do.get(parent.links[0][0])
                self.notify.error('Data file not found for area. connecting tunnel uid = %s' % tunnel.uniqueId)
            
            self.notify.error('Data file not found for area being loaded: %s, make sure worldCreator.loadObjectsFromFile is being called.' % parentUid)
        
        objDict = objectInfo.get('Objects')
        if objDict != None:
            self.loadObjectDict(objDict, parent, parentUid, dynamic, zoneLevel = zoneLevel, startTime = startTime)
            if objectInfo.has_key('AdditionalData'):
                additionalFiles = objectInfo['AdditionalData']
                for currFile in additionalFiles:
                    if self.fileDicts.has_key(currFile + '.py'):
                        altParentUid = self.fileDicts[currFile + '.py']['Objects'].keys()[0]
                        addObjDict = self.fileDicts[currFile + '.py']['Objects'][altParentUid]['Objects']
                        self.loadObjectDict(addObjDict, parent, parentUid, dynamic, zoneLevel = zoneLevel, startTime = startTime)
                        yieldThread('load object')
        
        fileRef = objectInfo.get('File')
        if fileRef:
            self.loadObjectsFromFile(fileRef + '.py', parent, parentUid, dynamic, zoneLevel = zoneLevel, startTime = startTime)
        
        if objectInfo.has_key('AdditionalData'):
            additionalFiles = objectInfo['AdditionalData']
            for currFile in additionalFiles:
                self.loadObjectsFromFile(currFile + '.py', parent, parentUid, dynamic, zoneLevel = zoneLevel, startTime = startTime, merge = True)

    def findObjectCategory(self, objectType):
        cats = ObjectList.AVAIL_OBJ_LIST.keys()
        for currCat in cats:
            types = ObjectList.AVAIL_OBJ_LIST[currCat].keys()
            if objectType in types:
                return currCat
        return None

    def createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel = 0, startTime = None, fileName = None, actualParentObj = None):
        objType = WorldCreatorBase.WorldCreatorBase.createObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel = zoneLevel, startTime = startTime, fileName = fileName)
        if objType == None:
            return (None, None)
        
        newObj = None
        objParent = None
        parentDoId = base.cr.uidMgr.getDoId(parentUid)
        if parentDoId:
            objParent = base.cr.doId2do.get(parentDoId)
            if objParent == None:
                self.notify.warning('Parent %s not found for %s' % (parentUid, objKey))
        
        if dynamic:
            objectCat = self.findObjectCategory(objType)
            if objType == 'Jack Sparrow Standin' and base.config.GetBool('want-npcs', 1) is 1:
                newObj = self.createJackSparrowStandin(object, objKey, objParent)
            elif objectCat == 'PROP_OBJ' or objectCat == 'BUILDING_OBJ':
                if objType == 'Light - Dynamic':
                    light = self.createDynamicLight(object, objParent)
                    if light:
                        base.cr.uidMgr.uid2obj[objKey] = light
                        objParent.addLight(light)
                    
                    OTPRender.renderReflection(False, light, 'p_light', None)
                elif objParent:
                    if object.has_key('Color'):
                        if not object.has_key('Visual'):
                            object['Visual'] = {}
                        
                        if not object['Visual'].has_key('Color'):
                            object['Visual']['Color'] = object['Color']
                    
                    self.propNum += 1
                    newObj = objParent.addChildObj(object, objKey, zoneLevel = zoneLevel, startTime = startTime, altParent = actualParentObj, actualParentObj = actualParentObj)
                    if newObj:
                        base.cr.uidMgr.uid2obj[objKey] = newObj
                        if objType in ('Pier', 'Dinghy'):
                            OTPRender.renderReflection(True, newObj, 'p_pier', None)

            elif objType == 'Cell Portal Area':
                newObj = objParent.addChildObj(object, objKey, zoneLevel = zoneLevel, startTime = startTime)
            elif objType == 'Event Sphere':
                newObj = self.addEventSphere(object, objParent)
            elif objType == 'Port Collision Sphere':
                pos = object.get('Pos', Point3(0, 0, 0))
                radius = object.get('Scale', VBase3(500))[0]
            elif objType == 'Location Sphere':
                newObj = self.addLocationSphere(objKey, object, objParent)
            
        elif objType == 'Player Spawn Node':
            if objParent:
                pos = object['Pos']
                hpr = object['Hpr']
                index = object.get('Index', -1)
                ownerPos = objParent.getPos()
                ownerHpr = objParent.getHpr()
                posHpr = (pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                self.cr.activeWorld.addPlayerSpawnPt(objParent, posHpr, index)
                newObj = posHpr
            
        elif objType == 'Player Boot Node':
            if objParent:
                pos = object['Pos']
                hpr = object['Hpr']
                tgtAreaUid = object['AreaUid']
                posHpr = (pos[0], pos[1], pos[2], hpr[0], hpr[1], hpr[2])
                self.cr.activeWorld.addPlayerBootPt(tgtAreaUid, posHpr, objParent.getDoId())
                newObj = posHpr
            
        elif objType == 'Cutscene Origin Node':
            if objParent:
                pos = object['Pos']
                hpr = object['Hpr']
                name = object['CutsceneId']
                node = objParent.attachNewNode(name)
                node.setPosHpr(pos, hpr)
                self.cr.activeWorld.addCutsceneOriginNode(node, name)
                newObj = node
            
        elif objType == 'Effect Node':
            if objParent:
                pos = object['Pos']
                hpr = object['Hpr']
                if object.has_key('Scale'):
                    scale = object['Scale']
                else:
                    scale = Point3(1.0, 1.0, 1.0)
                name = object['EffectName']
                node = objParent.attachNewNode(name)
                node.setPosHprScale(pos, hpr, scale)
                newObj = node
            
        if not objParent:
            self.notify.warning('No object parent located!')
            return (None, None)

        elif objType == 'Dinghy':
            newObj = objParent.addChildObj(object, objKey, zoneLevel = zoneLevel, startTime = startTime)
        elif objType == 'Holiday Object':
            newObj = objParent.addChildObj(object, objKey, zoneLevel = zoneLevel, startTime = startTime)
        
        return (newObj, None)

    def loadDataFile(self, fileName):
        self.fileDicts = {}
        self.loadObjectsFromFile(fileName, self.district)

    def loadObject(self, object, parent, parentUid, objKey, dynamic, zoneLevel = 0, startTime = None, parentIsObj = False, fileName = None, actualParentObj = None):
        (newObj, actualParentObj) = self.createObject(object, parent, parentUid, objKey, dynamic, zoneLevel = zoneLevel, startTime = startTime, fileName = fileName, actualParentObj = actualParentObj)
        objDict = object.get('Objects')
        if objDict:
            if newObj == None:
                
                callback = lambda param0 = 0, param1 = objDict, param2 = objKey, param3 = dynamic, param4 = -1: self.loadObjectDictDelayed(param0, param1, param2, param3, param4)
                base.cr.uidMgr.addUidCallback(objKey, callback)
            else:
                parentObj = newObj
                newParentUid = objKey
                if not isinstance(newObj, ClientArea.ClientArea):
                    parentObj = parent
                    newParentUid = parentUid
                
                self.loadObjectDict(objDict, parentObj, newParentUid, dynamic, zoneLevel = zoneLevel, startTime = startTime, actualParentObj = newObj)
        
        return newObj

    def loadObjectDictDelayed(self, parentObjDoId, objDict, parentUid, dynamic, zoneLevel = 0):
        parentObj = self.cr.doId2do[parentObjDoId]
        if hasattr(parentObj, 'loadZoneObjects'):
            parentObj.loadZoneObjects(zoneLevel)
        else:
            startTime = globalClock.getRealTime()
            self.loadObjectDict(objDict, parentObj, parentUid, dynamic, zoneLevel = zoneLevel, startTime = startTime)

    def addEventSphere(self, objData, objParent):
        objPos = objData['Pos']
        radius = objData['Scale'][0]
        category = objData['Event Type']
        extraParam = objData['Extra Param']
        collideType = PiratesGlobals.WallBitmask
        collType = objData['Collide Type']
        if collType == 'Ship':
            collideType = PiratesGlobals.ShipCollideBitmask
        elif collType == 'Object':
            collideType = PiratesGlobals.ShipCollideBitmask
        
        newEventSphere = CollisionSphere(objPos[0], objPos[1], objPos[2], radius)
        newEventSphere.setTangible(0)
        newEventSphereName = self.cr.activeWorld.uniqueName(extraParam) + str(id(newEventSphere))
        newEventSphereNode = CollisionNode(newEventSphereName)
        msgName = None
        if category == 'Port':
            msgName = PiratesGlobals.EVENT_SPHERE_PORT
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(collideType)
        elif category == 'Capture':
            msgName = PiratesGlobals.EVENT_SPHERE_CAPTURE
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(collideType)
        elif category == 'Sneak':
            newEventSphere.setTangible(1)
            msgName = PiratesGlobals.EVENT_SPHERE_SNEAK
            newEventSphereNode.setFromCollideMask(BitMask32.allOff())
            newEventSphereNode.setIntoCollideMask(collideType)
        elif category == 'Dock':
            pass
        elif category == 'DockWall':
            pass
        elif category in ['Spawning', 'Staging']:
            return None
        
        newEventSphereNode.addSolid(newEventSphere)
        newEventSphereNodePath = objParent.collisions.attachNewNode(newEventSphereNode)
        self.cr.activeWorld.accept('enter' + newEventSphereName, self.cr.activeWorld.enteredSphere, extraArgs = [
            [
                msgName,
                extraParam]])
        self.cr.activeWorld.accept('exit' + newEventSphereName, self.cr.activeWorld.exitedSphere, extraArgs = [
            [
                msgName,
                extraParam]])
        return newEventSphereNodePath
    
    def addLocationSphere(self, uid, objData, objParent):
        objPos = objData['Pos']
        radius = objData['Scale'][0]
        locName = objData.get('Area Name', '')
        collideType = PiratesGlobals.WallBitmask | PiratesGlobals.ShipCollideBitmask
        newSphere = CollisionSphere(objPos[0], objPos[1], objPos[2], radius)
        newSphere.setTangible(0)
        newSphereName = self.cr.activeWorld.uniqueName('locSphere')
        newSphereNode = CollisionNode(newSphereName)
        newSphereNode.setTag('uid', uid)
        newSphereNode.setTag('parentUid', objParent.getUniqueId())
        msgName = None
        msgName = PiratesGlobals.LOCATION_SPHERE
        newSphereNode.setFromCollideMask(BitMask32.allOff())
        newSphereNode.setIntoCollideMask(collideType)
        newSphereNode.addSolid(newSphere)
        newSphereNodePath = objParent.collisions.attachNewNode(newSphereNode)
        objParent.addLocationSphere(uid, objPos, radius, locName)
        return newSphereNodePath

    def createDynamicLight(self, objData, objParent):
        light = EditorGlobals.LightDynamic(objData, objParent, drawIcon = False)
        return light
    
    def createJackSparrowStandin(self, object, uid, parent):
        self.notify.debug('creating Jack')
        jack = Actor.Actor(object['Visual']['Model'], {
            'idle': 'models/char/js_idle',
            'walk': 'models/char/js_walk',
            'run': 'models/char/js_run'})
        jack.loop('idle')
        __builtins__['js'] = jack
        return parent.addChildObj(object, uid, objRef = jack)
    
    def loadAnimParts(self, object, objParent):
        effects = self.animPartsDict.get(object)
        intervals = Parallel()
        for effect in effects:
            myPart = effect[4]
            if effect[0] == 'Hpr':
                randomness = random.random() / 10
                rotate1 = myPart.hprInterval(effect[1] + randomness, effect[3], startHpr = effect[2], blendType = 'easeInOut')
                rotate2 = myPart.hprInterval(effect[1] + randomness, effect[2], startHpr = effect[3], blendType = 'easeInOut')
                anim = Sequence(rotate1, rotate2)
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'ColorFade':
                randomness = random.random() / 10
                fadeIn = myPart.colorInterval(effect[1] + randomness, effect[3], startColor = effect[2])
                fadeOut = myPart.colorInterval(effect[1] + randomness, effect[2], startColor = effect[3])
                anim = Sequence(fadeIn, fadeOut)
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'DelayColorFade':
                randomness = random.random() / 10
                fadeIn = myPart.colorInterval(effect[1] + randomness, effect[3], startColor = effect[2])
                fadeOut = myPart.colorInterval(effect[1] + randomness, effect[2], startColor = effect[3])
                anim = Sequence(fadeIn, Wait(effect[4]), fadeOut, Wait(effect[4]))
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'UVScroll':
                t = myPart.findAllTextureStages()[0]
                randomness = random.random() / 10
                anim = LerpFunctionInterval(self.setNewUVs, fromData = 0.0, toData = 10.0, duration = effect[1] + randomness, extraArgs = [
                    myPart,
                    t,
                    effect], name = 'UVScroll-%d')
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'UVOverlayScroll':
                t = TextureStage('t')
                t.setMode(TextureStage.MBlend)
                t.setSort(60)
                card = loader.loadModelCopy(effect[4])
                tex = card.findTexture('*')
                myPart.setTexture(t, tex)
                myPart.setTexScale(t, 2, 2)
                randomness = random.random() / 10
                anim = LerpFunctionInterval(self.setNewUVs, fromData = 0.0, toData = 10.0, duration = effect[1] + randomness, extraArgs = [
                    myPart,
                    t,
                    effect], name = 'UVOverlayScroll-%d')
                anim.loop()
                intervals.append(anim)
            elif effect[0] == 'Unlit':
                myPart.setDepthWrite(0)
                myPart.setColorScaleOff()
                myPart.setFogOff()
        
        return intervals
    
    def registerPostLoadCall(self, funcCall):
        self.postLoadCalls.append(funcCall)

    def processPostLoadCalls(self):
        functionsCalled = []
        for currObj in self.postLoadCalls:
            if currObj not in functionsCalled:
                functionsCalled.append(currObj)
                currObj()
        
        self.postLoadCalls = []


