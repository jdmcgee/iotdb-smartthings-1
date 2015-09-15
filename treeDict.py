#!/usr/bin/env python
import string
from hashlib import md5

class treeDictionary(dict):
    """
        description:
            this class produces a PA dictionary accessor class
        internal data structures:
            internalDictionary:
                this is a Python standard dictionary class it is the internal dictionary representation for the
                multitiered or tree you that the tree class exhibits.
            shortCuts:
                this is a standard Python dictionary class the primary key is the shortcut itself the value
                is the string representation of the shortcut
            shortCut keys:
                this is a Python list containing the key values of the shortcuts dictionary variable
             separator:
                this is a Python string that contains the character or string used to separate branch names
                and variable names in the tiered dictionary structure
            keyHashes
                this is a Python dictionary where the key is MD5 hex hash at a constant value. This
                list is used to perform the has key function and to look up whether or not I keep being
                tested actually exists in the internal dictionary
    """

    internalDictionary = None
    shortCuts = None
    shortCutKeys = None
    seperator = None
    keyHashes = None
    
    def __init__(self,baseDictionary={},baseShortCuts={},seperator="."):
        """
            initialization parameters:
                basedDictionary (default this {}) - this is the dictionary you wish to initialize the street
                    dictionary with.  this dictionary can be an multitiered dictionary. During
                    the initialization process all keys within the dictionary will be converted to the proper case and teiring
                baseShortCuts (default is {}) - this is a dictionary class containing the shortcuts to be used
                separator (default is ".") - this is a character string you wish to be used as a branch separator
                
        """
        self.internalDictionary = {}
        self.shortCuts = {}
        self.shortCutKeys = []
        self.seperator = seperator
        self.keyHashes = {}
        if baseDictionary=={}:
            self.internalDictionary = baseDictionary
        else:
            self.__setitem__(baseDictionary,None)
        if baseShortCuts!={}:
            self.addShortCutMap(baseShortCuts)
        self.shortCutKeys = self.shortCuts.keys()
        
    def convertKey(self,key):
        nKey = key
        if type(nKey)==type(()) or (type(nKey)==type("") and string.upper(nKey) in self.shortCutKeys):
            if type(nKey)==type(()):
                nKey,dataTuple  = nKey
                shortCut = self.shortCuts[string.upper(nKey)]
                nKey = shortCut % (dataTuple)
            else:
                nKey = self.shortCuts[string.upper(nKey)]
        if type(nKey)==type([]):
            nKey = string.join(nKey,self.seperator)
        return string.upper(nKey)
    def mkKeyList(self,key):
        nKey = key
        if type(key)!=type(""):
            nKey = self.convertKey(nKey)
        return map(string.upper,string.split(nKey,self.seperator))

    def getKeys(self, keyString):
        """
            description:
                this method will take a key strength and produce a list of brats elements.
            parameters:
                keyString - this is a string in the format 'word separator word separator word' or 'word.word.word' as an example
            return:
                a Python list containing the words used
        """
        return self.mkKeyList(keyString)

    def mkHash(self,key):
        """
            description:
                this method will take a list or a string key and produce a Md5 hex digest
            parameters:
                key - this can be a list or a string if it is a string that follows the same rules as and get keys.
            return:
                a string Md5 hex digest
        """
        tkey = self.convertKey(key)
        m5 = md5(tkey)
        return m5.hexdigest()
    def has_key(self,key):
        """
            description:
                this method will return true if the specified key exists in the internal dictionary digest or false
                if it does not
            parameters:
                key - this can be a list or a string if it is a string that follows the same rules as and get keys.
            return:
                true if he exists in the internal dictionary or false if it does not
        """
        tkey = self.mkHash(key)
        return tkey in self.keyHashes.keys()
    def addHashKey(self,key):
        """
            description:
                this method will add a hash key for the key specified into the internal hash list
            parameters:
                key - this can be a list or a string if it is a string that follows the same rules as and get keys.
            return:
                None
        """
        hashKey = self.mkHash(key)
        self.keyHashes[hashKey] = 1
    def rmHashKey(self,key):
        """
            description:
                this method will remove a hash key for the key specified into the internal hash list
            parameters:
                key - this can be a list or a string if it is a string that follows the same rules as and get keys.
            return:
                None
        """
        hashKey = self.mkHash(key)
        del self.keyHashes[hashKey]
    def addDictionary(self,dict,parent=""):
        keysToProcess = dict.keys()
        for key in keysToProcess:
            if type(dict[key])==type({}):
                if parent=="":
                    nkey = key
                else:
                    nkey = self.convertKey([parent,key])
                self[nkey] = {}
                self.addDictionary(dict[key],nkey)
            else:
                if parent=="":
                    nkey = key
                else:
                    nkey = self.convertKey([parent,key])
                self[nkey] = dict[key]
                
    def setDictItem(self,key,value):
        """
            description:
               this method will set an individual item within the tier dictionary structure
            parameters:
                key - this can be in several forms one being a standard string key and the other
                    being a string key plus a couple value this is used generally for shortcuts that have a specific namespace.
                value - this is the value to be set at the key location within the Teired Dictionary structure
            return:
                None
        """
        
        if type(key)==type({}):
            self.addDictionary(key)
        else:
            
            tkey = self.convertKey(key)
            self.addHashKey(tkey) 
            keys = self.getKeys(tkey)
            if len(keys)==1:
                self.internalDictionary[string.upper(keys[0])] = value
            else:
                itemKey = keys[-1]
                keys = keys[:-1]
                #keys.reverse()
                tdict = self.internalDictionary
                # test if keys exist
                for x in keys:
                    if not tdict.has_key(string.upper(x)):
                        tdict[string.upper(x)] = {}
                    if tdict[string.upper(x)]==None:
                        tdict[string.upper(x)] = {}
                    tdict = tdict[string.upper(x)]
                    
                        
                tdict[string.upper(itemKey)] = value

    def __setitem__(self,key,value):
        """
            description:
                this is the base class dictionary override to allow for the setting of items within the dictionary
            parameters:
                key - this can be in several forms one being a standard string key and the other
                    being a string key plus a couple value this is used generally for shortcuts that have a specific namespace.
                value - this is the value to be set at the key location within the Teired Dictionary structure
            return:
                None
        """
        self.setDictItem(key,value)

    def getDictItem(self,key):
        """
            description:
                this method will retrieve a value stored within a tiered dictionary structure
            parameters:
                key - this can be in several forms one being a standard string key and the other
                    being a string key plus a couple value this is used generally for shortcuts that have a specific namespace.
            return:
                the value pointed at by key within the tiered dictionary structure
        """
        tkey = self.convertKey(key)
        keys = self.getKeys(tkey)
        item = None
        if len(keys)==1:
            try:
                item = self.internalDictionary[string.upper(keys[0])]
            except:
                item = None
        else:
            try:
                tdict = self.internalDictionary
                for x in keys:
                    item = tdict[string.upper(x)]
                    tdict = item
            except:
                item = None
        return item
        
    def __getitem__(self,key):
        """
            description:
                    this is the base class dictionary override to allow for the getting of items within the dictionary
                parameters:
                    key - this can be in several forms one being a standard string key and the other
                        being a string key plus a couple value this is used generally for shortcuts that have a specific namespace.
                return:
                    the value pointed to by key within the tiered dictionary structure
            return self.getDictItem(key)
        """
        return self.getDictItem(key)
    
    def addShortCut(self,shortCut,key):
        """
            description:
                this method will add a shortcut to the key indexing system
            parameters:
                shortCut - this is the key within the shortcut dictionary to look up its actual meaning
                key - this is the actual key that the the shortcut points to. This key may contain variable
                    replacement parameters when used with specific names spaces
            return:
                None
        """
        self.shortCuts[string.upper(shortCut)] = key
        self.shortCutKeys = self.shortCuts.keys()
        
    def rmShortCut(self,shortCut):
        """
            description:
                this method will remove a shortcut from the shortcut dictionary
            parameters:
                shortCut - this is the key within the shortcut dictionary to be removed
            return:
                None
        """
        del self.shortCuts[string.upper(shortCut)]
        self.shortCutKeys = self.shortCuts.keys()
        
    def addShortCutMap(self,shortCutDict):
        """
            description:
                this method will take a shortcut dictionary and added to this current
                objects internal shortcut dictionary
            parameters:
                shortCutDict - this is a dictionary that contains shortcuts and key values
            return:
                None
            
        """
        for key in shortCutDict.keys():
            self.shortCuts[string.upper(key)] = shortCutDict[key]
        self.shortCutKeys = self.shortCuts.keys()
        
    def rmShortCuts(self,shortCutList):
        """
            description:
                this method will take a list of shortcut keys and remove them from the
                internal shortcut dictionary
            parameters:
                shortCutList - this is a Python list of key values
            return:
                None
        """
        for key in shortCutList:
            del self.shortCuts[string.upper(key)]
        self.shortCutKeys = self.shortCuts.keys()
        
    def __str__(self):
        """
            description:
                this is the based dictionary class Star function to produce a string
                representation of this object
            parameters:
                None
            return:
                a string representation of the internal dictionary structure. This is
                achieved by simply calling the str function of the internal dictionary
        """
        return self.internalDictionary.__str__()

