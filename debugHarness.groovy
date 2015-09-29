/* helper methods */

/* _logger
 * 	This is a debug logging function
 *
 * 	Example out put 
 *		<example here>
 * 	Parameters:
 *		methodName - The name of the method that is calling the _logger
 * 		lineMarker - Due to the smartthings limition to get the current line number it is intended to be a unique location identifyer
 *  	text - this is the text to be displayed
 * 	Returns:
 *		None
 *	Comments:
 *		The SmartThings execution envirmount has some limitions these are mainly due to security concerns understandability. One side effect
 *		if that most introspection abilities are out of scope for use and tend to return jave security exceptions. The example code below would 
 *		return a valid line number without these limitions.
 *
 *		--- Logging Utils --- 
 * 		def getCurrentMethodName(){
 * 			def marker = new Throwable()
 * 			return StackTraceUtils.sanitize(marker).stackTrace[1].methodName
 *		}
 * 		public static int getLineNumber() {
 *   		return Thread.currentThread().getStackTrace()[2].getLineNumber();
 *		}
 */
 
def _logger(methodName, lineMarker, text)
{
  def line = "${methodName}:${lineMarker} - ${text}"
  println line
}

def makeValue(value)
{
  return ["value":value]
}

def getStates(state,dev,rollUps)
{
    def states = [:]
    def value 
    def total = 0
    def stateIdx 
    def unAccountedTotal = 0
    def childTotal = 0
    def x = 0
    def finished = false
    while (finished == false)
    {
    	switch(x)
        {
        	case 0  :
            		stateIdx = state
            		/*_logger("getStates","A.20","else(${x}) state->${state} - dev.${state}.value")*/
                    break
            default:
            		stateIdx = "${state}${x}"
            		/*_logger("getStates","A.25","(${x}>0) state->${state} - dev.${state}.value")*/
                    break
        }
        _logger("getStates", "A.27", "passed case")
        
        if (dev.currentState("${stateIdx}")!=null)
        {
          _logger("getStates", "A.28", "In if")
          _logger("getStates", "A.28", "dev->${dev}")
          
        	value =  dev.currentState("${stateIdx}")
          _logger("getStates","A.30","stateIdx->${stateIdx}, value -> ${value}")
        	states[stateIdx] = value
            if (x>0 && value!=null)
            {
            	_logger("getStates","A.32", "(${stateIdx}) - value + childTotal(${childTotal} + ${value})")
            	childTotal = childTotal + value
                
            }
            x = x + 1
        }
        else
        {
        	_logger("getStates","A.40","Value is null")
        	finished = true
        }
       
    _logger("getStates", "A.45", "x->${x}")
    }
    if(rollUps)
    {
    	_logger("getStates","A.50","total->${total}")
        _logger("getStates","A.52", "childTotal->${childTotal}")
        states["total"] = total
        states["unAccountedTotal"] = total - childTotal
        states["childTotal"] = childTotal
    }
    _logger("getStates", "A.50","states->${states}")
    return states
}
/* SmartThings simulation classes
 *
 * Class Device - This simulates an SmartThings SmartApp Device
 *
 */

 class device
 {
    def name = ""
    def label = ""
    def id = ""
    
    def states = []
    public def device(name, label, id, states)
    {
      this.name = name
      this.label = label
      this.states = states
    }
    def addState(stateName, state)
    {
      this.states[stateName] = state
    }
    
    def currentState(stateIdx)
    {
      _logger("class device - currentState ", "A.10", "this.states[" + "${stateIdx}" +"] -> ${this.states[stateIdx]}")
      def value = this.states[stateIdx].value
      _logger("class device - returning ", "A.20", "${value}")
      return value
    }
    def _logger(methodName, lineMarker, text)
    {
      def line = "${methodName}:${lineMarker} - ${text}"
      println line
    }
 }
 




def getStatesDebug()
{
  _logger("getStatesDebug", "A.10", "Start of debug Session")
  /* Data setup */
  def id = "abe801ad-b07e-4bcc-9b8c-b26bae2cb099"
  def name = "Aeon SmartStrip"
  def label ="Aeon Ss 01"
  
  
  def states = [energyState:[value:236.32],
                energyState1:[value:51.31],
                energyState2:[value:17.49],
                energyState3:[value:27.7],
                energyState4:[value:53.23],
                powerState:[value:256],
                powerState1:[value:119],
                powerState2:[value:17],
                powerState3:[value:40],
                powerState4:[value:82],
                switchState:[value:"on"],
                switchState1:[value:"on"],
                switchState2:[value:"on"],
                switchState3:["value":"on"],
                switchState4:[value:"on"]
              ]
  def dev = new device(name, label, id, states)
  
  println "${getStates("energyState",dev,true)}"
}
  
  
getStatesDebug()