import numpy as np

class AllocatedPiece1D:
    """ /**
     * A class representing a piece allocated on a 1-dimensional cake to an agent with a given value-function.
     *
     * @author Erel Segal-Halevi
     * @since 2016-11
     */"""

     def __init__(self, valueFunction, iFrom, iTo):
         """ /**
         *  Initialize a 1-dimensional allocated piece based on a value function.
         *  @param valueFunction a ValueFunction1D.
         *  @param iFrom (float) start of allocation.
         *  @param iTo (float) end of allocation.
         */ """
    	if iFrom is None: iFrom = 0
    	if iTo is None:   iTo = valueFunction.values.length

    	self.valueFunction = valueFunction
    	self.iFrom = iFrom
    	self.iTo = iTo

    def getCut(self, value):
		"""
		The current agent decides where to cut his current allocation
		such that the cut piece will have the specified value.
		"""
		return self.valueFunction.getCut(self.iFrom, value)

    def getValue(self):
		"""
		The current agent evaluates his own piece.
		"""
		return self.valueFunction.getValue(self.iFrom, self.iTo)

    def getValueOfOther(self, other):
        """
        The current agent evaluates a piece allocated to another agent.
        """
        return self.valueFunction.getValue(other.iFrom, other.iTo);

    def getRelativeValue(self):
        """
        The current agent evaluates his own piece relative to the entire cake.
        """
        return self.valueFunction.getRelativeValue(self.iFrom, self.iTo)
