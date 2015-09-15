#!/usr/bin/env python

class data_has_no_device_info(Exception):
  def __init__(self,value):
    self.data = value
  
  def __str__(self):
    print self.data.__str__()
  
class data_has_no_name_info(Exception):
  def __init__(self,value):
    self.data = value
  
  def __str__(self):
    print self.data.__str__()

class data_not_for_this_device(Exception):
  def __init__(self,value):
    self.validNames, self.data = value
  
  def __str__(self):
    print self.vaidNames.__str(), self.data.__str__()
    
class no_data(Exception):
  def __init__(self,value):
    self.data = value
  
  def __str__(self):
    print self.data.__str__()
    
class invalid_child_name(Exception):
  self.childName, self.allowedNames = value
  
  def __str__(self):
    return "invalid Child Name %s allowed Names are %s" % (self.childName. self.allowedNames)
  
class invalid_item_name(Exception):
  self.childName, self.allowedNames = value
  
  def __str__(self):
    return "invalid Item Name %s allowed Names are %s" % (self.childName. self.allowedNames)
  
stDevicesSchema = {
                    "devices.%s" : {},
                    "objects" : {},
                    "motionSensors" : {},
                    "rooms" : {}
                  }

stShortcuts =   {
                  "device"   : "devices.%s",
                  "device.id" : "devices.%s.id",
                  "device.name": "devices.%s.name",
                  "device.label": "devices.%s.label",
                  "battery"  : "devices.%s.battery",
                  "battery.date" :  "devices.%s.battery.date",
                  "battery.name" : "devices.%s.battery.name",
                  "battery.type" : "devices.%s.battery.type",
                  "battery.unit"  : "devices.%s.battery.unit",
                  "battery.unixTime" : "devices.%s.battery.unixTime",
                  "battery.value" : "devices.%s.battery.value",
                  "motion"  : "devices.%s.motion",
                  "motion.date" :  "devices.%s.motion.date",
                  "motion.name" : "devices.%s.motion.name",
                  "motion.type" : "devices.%s.motion.type",
                  "motion.unit"  : "devices.%s.motion.unit",
                  "motion.unixTime" : "devices.%s.motion.unixTime",
                  "motion.value" : "devices.%s.motion.value",
                  "temperature"  : "devices.%s.temperature",
                  "temperature.date" :  "devices.%s.temperature.date",
                  "temperature.name" : "devices.%s.temperature.name",
                  "temperature.type" : "devices.%s.temperature.type",
                  "temperature.unit"  : "devices.%s.temperature.unit",
                  "temperature.unixTime" : "devices.%s.temperature.unixTime",
                  "temperature.value" : "devices.%s.temperature.value",
                  "temperature.temp" : "devices.%s.temperature.value",
                  
                  "object" : "objects.%s",
                  "motionSensor" : "motionSensors.%s",
                  
                  "childData" : "devices.%s.%s.%s"
                }

class motionSensor(treeDictionary):
  validDevNames = ["SmartSense Motion/Temp Sensor"]
  allowedChildren = ["battery", "motion", "temperature" ]
  allowedItemNames = ["name","date","type","unit","unixtime","value","temp"]
  
  def __init__(self, dataset, data=None):
    self.dataset = dataset
    self.id = None
    
    if data:
      self.pouplate(data)


  def populate(self,data):
    if not data.has_key(device):
      # throw data has no device info
      raise data_has_not_device_info(data)
  
    
    if not data["device"].has_key("name"):
      # throw device has no name
      raise data_has_no_name_info(data)
    
    if data["device"]["name"] not in self.validDevNames:
      # data not for this device
      raise data_not_for_his_device((self.validDevNames,data))
    
    
    self.id = data["device"]["id"]
    self.label = data["device"]["label"]
    self.name = data["device"]["name"]
    self.dataset["device",(self.id)] = {}
    self.dataset["device.id",(self.id)] = self.id
    self.dataset["device.name",(self.id)] = self.name
    self.dataset["device.label",(self.id)] = self.label
    # extract children form data
    children = data["children"]
    # battery details
    
    dataObj = children["battery"]
    self["battery", (self.id)] = {}
    self.dataset["battery.date",(self.id)] = dataObj["date"]
    self.dataset["battery.name",(self.id)] = dataObj["name"]
    self.dataset["battery.type", (self.id)] = dataObj["type"]
    self.dataset["battery.unit", (self.id)] = dataObj["unit"]
    self.dataset["battery.unixTime",(self.id)] = dataObj["unitTime"]
    self.dataset["battery.value",(self.id)] = dataObj["value"]
    
    # motion details
    dataObj = children["motion"]
    self["motion", (self.id)] = {}
    self.dataset["motion.date",(self.id)] = dataObj["date"]
    self.dataset["motion.name",(self.id)] = dataObj["name"]
    self.dataset["motion.type", (self.id)] = dataObj["type"]
    self.dataset["motion.unit", (self.id)] = dataObj["unit"]
    self.dataset["motion.unixTime",(self.id)] = dataObj["unitTime"]
    self.dataset["motion.value",(self.id)] = dataObj["value"]
    
    # motion details
    dataObj = children["temperature"]
    self["temperature", (self.id)] = {}
    self.dataset["temperature.date",(self.id)] = dataObj["date"]
    self.dataset["temperature.name",(self.id)] = dataObj["name"]
    self.dataset["temperature.type", (self.id)] = dataObj["type"]
    self.dataset["temperature.unit", (self.id)] = dataObj["unit"]
    self.dataset["temperature.unixTime",(self.id)] = dataObj["unitTime"]
    self.dataset["temperature.value",(self.id)] = dataObj["value"]
    
    # set object reference
    self.dataset["object",(self.id)] = self
    # set motions sensor reference
    self.dataset["motionSensor", (self.id)] = object
    
  
  def getId(self):
    if not self.id:
      raise no_data("id")
    
    return self.id
  
  def getLabel(self):
    if not self.label:
      raise no_data("label")
    
    return self.label
  
  def getName(self):
    if not self.name:
      raise no_data("name")
    return self.name
  
  def getChildData(self,childName,itemName):
    if childName.lower() not in self.allowedChildren:
      raise invalid_child_name((childName,self.allowedChildren))
    
    if itemName.lower() not in self.allowedItemNames:
      raise invalid_item_name((itemName,self.allowedItemNames))
      
    return self.dataset["childData",self.id,childName,itemName]
  
class powerStrip:
  pass
