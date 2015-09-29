lass data_has_no_device_info(Exception):
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
  def __init__(self,value):
    self.childName, self.allowedNames = value
  
  def __str__(self):
    return "invalid Child Name %s allowed Names are %s" % (self.childName. self.allowedNames)
  
class invalid_item_name(Exception):
  def __init__(self,value):
    self.childName, self.allowedNames = value
  
  def __str__(self):
    return "invalid Item Name %s allowed Names are %s" % (self.childName. self.allowedNames)
 