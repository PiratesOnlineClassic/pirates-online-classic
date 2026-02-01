from enum import Enum as PyEnum
from functools import cmp_to_key
import math
from direct.showbase import DConfig

def Enum(*args):
    if len(args) == 1:
        arg = args[0]
        start = 0
    elif len(args) == 2:
        arg = args[0]
        start = args[1]
    else:
        raise ValueError("Enum expects 1 or 2 arguments")
    if isinstance(arg, list):
        names = arg
    else:
        names = [name.strip() for part in arg.split(',') for name in part.split() if name.strip()]
    E = PyEnum('Enum', names, start=start)

    # Backwards-compatible helper: return a string name for an enum
    # value when code expects a getString() function on the enum.
    def _getString(item):
        try:
            return item.name
        except Exception:
            return str(item)

    # Attach as a staticmethod on the generated Enum class.
    setattr(E, 'getString', staticmethod(_getString))

    return E

def getSetterName(valueName, prefix='set'):
    # getSetterName('color') -> 'setColor'
    # getSetterName('color', 'get') -> 'getColor'
    return '%s%s%s' % (prefix, valueName[0].upper(), valueName[1:])
def getSetter(targetObj, valueName, prefix='set'):
    # getSetter(smiley, 'pos') -> smiley.setPos
    return getattr(targetObj, getSetterName(valueName, prefix))

def mostDerivedLast(classList):
    """pass in list of classes. sorts list in-place, with derived classes
    appearing after their bases"""
    def compare(a, b):
        if issubclass(a, b):
            result=1
        elif issubclass(b, a):
            result=-1
        else:
            result=0
        #print a, b, result
        return result
    classList.sort(key=cmp_to_key(compare))

def makeTuple(x):
    if isinstance(x, tuple):
        return x
    elif isinstance(x, list):
        return tuple(x)
    else:
        return (x,)

def invertDict(d):
    return {v: k for k, v in d.items()}

def Functor(function, *args, **kArgs):
    argsCopy = args[:]
    def functor(*cArgs, **ckArgs):
        kArgs.update(ckArgs)
        return function(*(argsCopy + cArgs), **kArgs)
    return functor

class ScratchPad:
    """empty class to stick values onto"""
    def __init__(self, **kArgs):
        for key, value in kArgs.items():
            setattr(self, key, value)
        self._keys = set(kArgs.keys())
    def add(self, **kArgs):
        for key, value in kArgs.items():
            setattr(self, key, value)
        self._keys.update(kArgs.keys())
    def destroy(self):
        for key in self._keys:
            delattr(self, key)
    # allow dict [] syntax
    def __getitem__(self, itemName):
        return getattr(self, itemName)
    def get(self, itemName, default=None):
        return getattr(self, itemName, default)

class ParamObj:
    # abstract base for classes that want to support a formal parameter
    # set whose values may be queried, changed, 'bulk' changed (defer reaction
    # to changes until multiple changes have been performed), and
    # extracted/stored/applied all at once (see documentation above)

    # ParamSet subclass: container of parameter values. Derived class must
    # derive a new ParamSet class if they wish to define new params. See
    # documentation above.
    class ParamSet:
        Params = {
            # base class does not define any parameters, but they would
            # appear here as 'name': defaultValue,
            #
            # WARNING: default values of mutable types that do not copy by
            # value (dicts, lists etc.) will be shared by all class instances
            # if default value is callable, it will be called to get actual
            # default value
            #
            # for example:
            #
            # class MapArea(ParamObj):
            #     class ParamSet(ParamObj.ParamSet):
            #         Params = {
            #             'spawnIndices': Functor(list, [1,5,22]),
            #         }
            #
            }

        def __init__(self, *args, **kwArgs):
            self.__class__._compileDefaultParams()
            if len(args) == 1 and len(kwArgs) == 0:
                # extract our params from an existing ParamObj instance
                obj = args[0]
                self.paramVals = {}
                for param in self.getParams():
                    self.paramVals[param] = getSetter(obj, param, 'get')()
            else:
                assert len(args) == 0
                if __debug__:
                    for arg in kwArgs.keys():
                        assert arg in self.getParams()
                self.paramVals = dict(kwArgs)
        def getValue(self, param):
            if param in self.paramVals:
                return self.paramVals[param]
            return self._Params[param]
        def applyTo(self, obj):
            # Apply our entire set of params to a ParamObj
            obj.lockParams()
            for param in self.getParams():
                getSetter(obj, param)(self.getValue(param))
            obj.unlockParams()
        def extractFrom(self, obj):
            # Extract our entire set of params from a ParamObj
            obj.lockParams()
            for param in self.getParams():
                self.paramVals[param] = getSetter(obj, param, 'get')()
            obj.unlockParams()
        @classmethod
        def getParams(cls):
            # returns safely-mutable list of param names
            cls._compileDefaultParams()
            return cls._Params.keys()
        @classmethod
        def getDefaultValue(cls, param):
            cls._compileDefaultParams()
            dv = cls._Params[param]
            if hasattr(dv, '__call__'):
                dv = dv()
            return dv
        @classmethod
        def _compileDefaultParams(cls):
            if '_Params' in cls.__dict__:
                # we've already compiled the defaults for this class
                return
            bases = list(cls.__bases__)
            # bring less-derived classes to the front
            mostDerivedLast(bases)
            cls._Params = {}
            for c in (bases + [cls]):
                # make sure this base has its dict of param defaults
                if hasattr(c, '_compileDefaultParams'):
                    c._compileDefaultParams()
                if 'Params' in c.__dict__:
                    # apply this class' default param values to our dict
                    cls._Params.update(c.Params)
        def __repr__(self):
            argStr = ''
            for param in self.getParams():
                argStr += '%s=%s,' % (param,
                                      repr(self.getValue(param)))
            return '%s.%s(%s)' % (
                self.__class__.__module__, self.__class__.__name__, argStr)
    # END PARAMSET SUBCLASS

    def __init__(self, *args, **kwArgs):
        assert issubclass(self.ParamSet, ParamObj.ParamSet)
        # If you pass in a ParamSet obj, its values will be applied to this
        # object in the constructor.
        params = None
        if len(args) == 1 and len(kwArgs) == 0:
            # if there's one argument, assume that it's a ParamSet
            params = args[0]
        elif len(kwArgs) > 0:
            assert len(args) == 0
            # if we've got keyword arguments, make a ParamSet out of them
            params = self.ParamSet(**kwArgs)

        self._paramLockRefCount = 0
        # these hold the current value of parameters while they are being set to
        # a new value, to support getPriorValue()
        self._curParamStack = []
        self._priorValuesStack = []

        # insert stub funcs for param setters, to handle locked params
        for param in self.ParamSet.getParams():

            # set the default value on the object
            setattr(self, param, self.ParamSet.getDefaultValue(param))
            
            setterName = getSetterName(param)
            getterName = getSetterName(param, 'get')

            # is there a setter defined?
            if not hasattr(self, setterName):
                # no; provide the default
                def defaultSetter(self, value, param=param):
                    #print '%s=%s for %s' % (param, value, id(self))
                    setattr(self, param, value)
                setattr(self.__class__, setterName, defaultSetter)

            # is there a getter defined?
            if not hasattr(self, getterName):
                # no; provide the default. If there is no value set, return
                # the default
                def defaultGetter(self, param=param,
                                  default=self.ParamSet.getDefaultValue(param)):
                    return getattr(self, param, default)
                setattr(self.__class__, getterName, defaultGetter)

            # have we already installed a setter stub?
            origSetterName = '%s_ORIG' % (setterName,)
            if not hasattr(self, origSetterName):
                # move the original setter aside
                origSetterFunc = getattr(self.__class__, setterName)
                setattr(self.__class__, origSetterName, origSetterFunc)
                """
                # if the setter is a direct member of this instance, move the setter
                # aside
                if setterName in self.__dict__:
                    self.__dict__[setterName + '_MOVED'] = self.__dict__[setterName]
                    setterFunc = self.__dict__[setterName]
                    """
                # install a setter stub that will a) call the real setter and
                # then the applier, or b) call the setter and queue the
                # applier, depending on whether our params are locked
                """
                setattr(self, setterName, new.instancemethod(
                    Functor(setterStub, param, setterFunc), self, self.__class__))
                    """
                def setterStub(self, value, param=param, origSetterName=origSetterName):
                    # should we apply the value now or should we wait?
                    # if this obj's params are locked, we track which values have
                    # been set, and on unlock, we'll call the applyers for those
                    # values
                    if self._paramLockRefCount > 0:
                        priorValues = self._priorValuesStack[-1]
                        if param not in priorValues:
                            try:
                                priorValue = getSetter(self, param, 'get')()
                            except:
                                priorValue = None
                            priorValues[param] = priorValue
                        self._paramsSet[param] = None
                        getattr(self, origSetterName)(value)
                    else:
                        # prepare for call to getPriorValue
                        try:
                            priorValue = getSetter(self, param, 'get')()
                        except:
                            priorValue = None
                        self._priorValuesStack.append({
                            param: priorValue,
                            })
                        getattr(self, origSetterName)(value)
                        # call the applier, if there is one
                        applier = getattr(self, getSetterName(param, 'apply'), None)
                        if applier is not None:
                            self._curParamStack.append(param)
                            applier()
                            self._curParamStack.pop()
                        self._priorValuesStack.pop()
                        if hasattr(self, 'handleParamChange'):
                            self.handleParamChange((param,))

                setattr(self.__class__, setterName, setterStub)

        if params is not None:
            params.applyTo(self)

    def destroy(self):
        """
        for param in self.ParamSet.getParams():
            setterName = getSetterName(param)
            self.__dict__[setterName].destroy()
            del self.__dict__[setterName]
            """
        pass
    
    def setDefaultParams(self):
        # set all the default parameters on ourself
        self.ParamSet().applyTo(self)

    def getCurrentParams(self):
        params = self.ParamSet()
        params.extractFrom(self)
        return params

    def lockParams(self):
        self._paramLockRefCount += 1
        if self._paramLockRefCount == 1:
            self._handleLockParams()
    def unlockParams(self):
        if self._paramLockRefCount > 0:
            self._paramLockRefCount -= 1
            if self._paramLockRefCount == 0:
                self._handleUnlockParams()
    def _handleLockParams(self):
        # this will store the names of the parameters that are modified
        self._paramsSet = {}
        # this will store the values of modified params (from prior to
        # the lock).
        self._priorValuesStack.append({})
    def _handleUnlockParams(self):
        for param in self._paramsSet:
            # call the applier, if there is one
            applier = getattr(self, getSetterName(param, 'apply'), None)
            if applier is not None:
                self._curParamStack.append(param)
                applier()
                self._curParamStack.pop()
        self._priorValuesStack.pop()
        if hasattr(self, 'handleParamChange'):
            self.handleParamChange(tuple(self._paramsSet.keys()))
        del self._paramsSet
    def paramsLocked(self):
        return self._paramLockRefCount > 0
    def getPriorValue(self):
        # call this within an apply function to find out what the prior value
        # of the param was
        return self._priorValuesStack[-1][self._curParamStack[-1]]

    def __repr__(self):
        argStr = ''
        for param in self.ParamSet.getParams():
            try:
                value = getSetter(self, param, 'get')()
            except:
                value = '<unknown>'
            argStr += '%s=%s,' % (param, repr(value))
        return '%s(%s)' % (self.__class__.__name__, argStr)

if __debug__:
    class ParamObjTest(ParamObj):
        class ParamSet(ParamObj.ParamSet):
            Params = {
                'num': 0,
            }
        def applyNum(self):
            self.priorValue = self.getPriorValue()
    pto = ParamObjTest()
    assert pto.getNum() == 0
    pto.setNum(1)
    assert pto.priorValue == 0
    assert pto.getNum() == 1
    pto.lockParams()
    pto.setNum(2)
    # make sure applyNum is not called until we call unlockParams
    assert pto.priorValue == 0
    assert pto.getNum() == 2
    pto.unlockParams()
    assert pto.priorValue == 1
    assert pto.getNum() == 2

class POD:
    DataSet = {
        # base class does not define any data items, but they would
        # appear here as 'name': defaultValue,
        #
        # WARNING: default values of mutable types that do not copy by
        # value (dicts, lists etc.) will be shared by all class instances.
        # if default value is callable, it will be called to get actual
        # default value
        #
        # for example:
        #
        # class MapData(POD):
        #     DataSet = {
        #         'spawnIndices': Functor(list, [1,5,22]),
        #         }
        }
    def __init__(self, **kwArgs):
        self.__class__._compileDefaultDataSet()
        if __debug__:
            # make sure all of the keyword arguments passed in
            # are present in our data set
            for arg in kwArgs.keys():
                assert arg in self.getDataNames(), (
                    "unknown argument for %s: '%s'" % (
                    self.__class__, arg))
        # assign each of our data items directly to self
        for name in self.getDataNames():
            # if a value has been passed in for a data item, use
            # that value, otherwise use the default value
            if name in kwArgs:
                getSetter(self, name)(kwArgs[name])
            else:
                getSetter(self, name)(self.getDefaultValue(name))

    def setDefaultValues(self):
        # set all the default data values on ourself
        for name in self.getDataNames():
            getSetter(self, name)(self.getDefaultValue(name))
    # this functionality used to be in the constructor, triggered by a single
    # positional argument; that was conflicting with POD subclasses that wanted
    # to define different behavior for themselves when given a positional
    # constructor argument
    def copyFrom(self, other, strict=False):
        # if 'strict' is true, other must have a value for all of our data items
        # otherwise we'll use the defaults
        for name in self.getDataNames():
            if hasattr(other, getSetterName(name, 'get')):
                setattr(self, name, getSetter(other, name, 'get')())
            else:
                if strict:
                    raise "object '%s' doesn't have value '%s'" % (other, name)
                else:
                    setattr(self, name, self.getDefaultValue(name))
        # support 'p = POD.POD().copyFrom(other)' syntax
        return self
    def makeCopy(self):
        # returns a duplicate of this object
        return self.__class__().copyFrom(self)
    def applyTo(self, obj):
        # Apply our entire set of data to another POD
        for name in self.getDataNames():
            getSetter(obj, name)(getSetter(self, name, 'get')())
    def getValue(self, name):
        return getSetter(self, name, 'get')()

    @classmethod
    def getDataNames(cls):
        # returns safely-mutable list of datum names
        cls._compileDefaultDataSet()
        return cls._DataSet.keys()
    @classmethod
    def getDefaultValue(cls, name):
        cls._compileDefaultDataSet()
        dv = cls._DataSet[name]
        # this allows us to create a new mutable object every time we ask
        # for its default value, i.e. if the default value is dict, this
        # method will return a new empty dictionary object every time. This
        # will cause problems if the intent is to store a callable object
        # as the default value itself; we need a way to specify that the
        # callable *is* the default value and not a default-value creation
        # function
        if hasattr(dv, '__call__'):
            dv = dv()
        return dv
    @classmethod
    def _compileDefaultDataSet(cls):
        if '_DataSet' in cls.__dict__:
            # we've already compiled the defaults for this class
            return
        # create setters & getters for this class
        if 'DataSet' in cls.__dict__:
            for name in cls.DataSet:
                setterName = getSetterName(name)
                if not hasattr(cls, setterName):
                    def defaultSetter(self, value, name=name):
                        setattr(self, name, value)
                    setattr(cls, setterName, defaultSetter)
                getterName = getSetterName(name, 'get')
                if not hasattr(cls, getterName):
                    def defaultGetter(self, name=name):
                        return getattr(self, name)
                    setattr(cls, getterName, defaultGetter)
        # this dict will hold all of the aggregated default data values for
        # this particular class, including values from its base classes
        cls._DataSet = {}
        bases = list(cls.__bases__)
        # process in reverse of inheritance order, so that base classes listed first
        # will take precedence over later base classes
        bases.reverse()
        for curBase in bases:
            # skip multiple-inheritance base classes that do not derive from POD
            if issubclass(curBase, POD):
                # make sure this base has its dict of data defaults
                curBase._compileDefaultDataSet()
                # grab all inherited data default values
                cls._DataSet.update(curBase._DataSet)
        # pull in our own class' default values if any are specified
        if 'DataSet' in cls.__dict__:
            cls._DataSet.update(cls.DataSet)

    def __repr__(self):
        argStr = ''
        for name in self.getDataNames():
            argStr += '%s=%s,' % (name, repr(getSetter(self, name, 'get')()))
        return '%s(%s)' % (self.__class__.__name__, argStr)

if __debug__:
    class PODtest(POD):
        DataSet = {
            'foo': dict,
            }
    p1 = PODtest()
    p2 = PODtest()
    assert hasattr(p1, 'foo')
    # make sure the getter is working
    assert p1.getFoo() is p1.foo
    p1.getFoo()[1] = 2
    assert p1.foo[1] == 2
    # make sure that each instance gets its own copy of a mutable
    # data item
    assert p1.foo is not p2.foo
    assert len(p1.foo) == 1
    assert len(p2.foo) == 0
    # make sure the setter is working
    p2.setFoo({10:20})
    assert p2.foo[10] == 20
    # make sure modifications to mutable data items don't affect other
    # instances
    assert p1.foo[1] == 2

    class DerivedPOD(PODtest):
        DataSet = {
            'bar': list,
            }
    d1 = DerivedPOD()
    # make sure that derived instances get their own copy of mutable
    # data items
    assert hasattr(d1, 'foo')
    assert len(d1.foo) == 0
    # make sure derived instances get their own items
    assert hasattr(d1, 'bar')
    assert len(d1.bar) == 0

class HotkeyBreaker:
    def __init__(self,breakKeys = []):
        from direct.showbase.DirectObject import DirectObject
        self.do = DirectObject()
        self.breakKeys = {}
        if not isinstance(breakKeys, (list,tuple)):
            breakKeys = (breakKeys,)
        for key in breakKeys:
            self.addBreakKey(key)
        
    def addBreakKey(self,breakKey):
        if __dev__:
            self.do.accept(breakKey,self.breakFunc,extraArgs = [breakKey])
        
    def removeBreakKey(self,breakKey):
        if __dev__:
            self.do.ignore(breakKey)

    def breakFunc(self,breakKey):
        if __dev__:
            self.breakKeys[breakKey] = True

    def setBreakPt(self, breakKey = None, persistent = False):
        if __dev__:
            if not breakKey:
                import pdb;pdb.set_trace()
                return True
            else:
                if self.breakKeys.get(breakKey,False):
                    if not persistent:
                        self.breakKeys.pop(breakKey)
                    import pdb;pdb.set_trace()
                    return True
        return True

    def clearBreakPt(self, breakKey):
        if __dev__:
            return bool(self.breakKeys.pop(breakKey,None))
        
def pivotScalar(scalar, pivot):
    # reflect scalar about pivot; see tests below
    return pivot + (pivot - scalar)

if __debug__:
    assert pivotScalar(1, 0) == -1
    assert pivotScalar(-1, 0) == 1
    assert pivotScalar(3, 5) == 7
    assert pivotScalar(10, 1) == -8

rad90 = math.pi / 2.
rad180 = math.pi
rad270 = 1.5 * math.pi
rad360 = 2. * math.pi

def reduceAngle(deg):
    """
    Reduces an angle (in degrees) to a value in [-180..180)
    """
    return (((deg + 180.) % 360.) - 180.)

def lerp(a, b, t):
    return a + (b - a) * t

def clampScalar(value, minVal, maxVal):
    return max(minVal, min(value, maxVal))

def get_config_showbase():
    return DConfig

def get_config_express():
    return DConfig

getConfigShowbase = get_config_showbase
getConfigExpress = get_config_express

def recordFunctorCreationStacks():
    global Functor
    config = getConfigShowbase()
    # off by default, very slow
    if __dev__ and config.GetBool('record-functor-creation-stacks', 0):
        if not hasattr(Functor, '_functorCreationStacksRecorded'):
            Functor = recordCreationStackStr(Functor)
            Functor._functorCreationStacksRecorded = True
            Functor.__call__ = Functor._exceptionLoggedCreationStack__call__

class ScratchPad:
    """empty class to stick values onto"""
    def __init__(self, **kArgs):
        for key, value in kArgs.items():
            setattr(self, key, value)
        self._keys = set(kArgs.keys())
    def add(self, **kArgs):
        for key, value in kArgs.items():
            setattr(self, key, value)
        self._keys.update(kArgs.keys())
    def destroy(self):
        for key in self._keys:
            delattr(self, key)

    # allow dict [] syntax
    def __getitem__(self, itemName):
        return getattr(self, itemName)
    def get(self, itemName, default=None):
        return getattr(self, itemName, default)
    # allow 'in'
    def __contains__(self, itemName):
        return itemName in self._keys

class DestructiveScratchPad(ScratchPad):
    # automatically calls destroy() on elements passed to __init__
    def add(self, **kArgs):
        for key, value in kArgs.items():
            if hasattr(self, key):
                getattr(self, key).destroy()
            setattr(self, key, value)
        self._keys.update(kArgs.keys())
    def destroy(self):
        for key in self._keys:
            getattr(self, key).destroy()
        ScratchPad.destroy(self)