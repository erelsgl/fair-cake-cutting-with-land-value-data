import numpy as np
from functools import lru_cache


class ValueFunction1D:
	"""/**
	* A class that represents a 1-dimensional piecewise-constant function.
	*
	* @author Erel Segal-Halevi
	* @since 2016-11
	*/"""

	def __init__(self, values):
		"""
		values are the constant values.
		E.g, if values = [1,3,2], then the function equals 1 on [0,1], 3 on [1,2] and 2 on [2,3].
		"""
		self.values = np.array(values)
		self.length = len(values)

	def sum(self, iFrom, iTo):
		""" /**
		* Given iFrom and iTo, calculate sum
		* @param iFrom a float index.
		* @param iTo a float index.
		* @return the sum of the array between the indices (as float).
		*
	    >>> a = ValueFunction1D([1,2,3,4])
	    >>> a.sum(1,3)
	    5.0
	    >>> a.sum(1.5,3)
	    4.0
	    >>> a.sum(1,3.25)
	    6.0
	    >>> a.sum(1.5,3.25)
	    5.0
		>>>
		*
		*/ """
		if iFrom<0 or iFrom>self.length:
			raise ValueError("iFrom out of range: "+iFrom)
		if iTo<0 or iTo>self.length:
			raise ValueError("iTo out of range: "+iTo)
		if iTo<=iFrom:
			return 0  # special case not covered by loop below

		fromFloor = int(np.floor(iFrom))
		fromFraction = (fromFloor+1-iFrom)
		toCeiling = int(np.ceil(iTo))
		toCeilingRemovedFraction = (toCeiling-iTo)

		sum = 0.0;
		sum += (self.values[fromFloor]*fromFraction)
		sum += self.values[fromFloor+1:toCeiling].sum()
		sum -= (self.values[toCeiling-1]*toCeilingRemovedFraction)

		return sum

	def invSum(self, iFrom, sum):
		""" /**
		* Given iFrom and sum, calculate iTo
		* @param iFrom a float index.
		* @param sum the required sum.
		* @return the final index "iTo", such that sum(values,iFrom,iTo)=sum
	    >>> a = ValueFunction1D([1,2,3,4])
	    >>> a.invSum(1, 5)
	    3.0
	    >>> a.invSum(1.5, 4)
	    3.0
	    >>> a.invSum(1, 6)
	    3.25
	    >>> a.invSum(1.5,5)
	    3.25
		>>>
		*
		*/ """
		if iFrom<0 or iFrom>self.length:
			raise ValueError("iFrom out of range: "+iFrom)
		if sum<0:
			raise ValueError("sum out of range (should be positive): "+sum)

		iFrom = float(iFrom)
		fromFloor = int(np.floor(iFrom));
		fromFraction = (fromFloor+1-iFrom);

		value = self.values[fromFloor];
		if value*fromFraction >= sum:
			return iFrom + (sum/value);
		sum -= (value*fromFraction);
		for i in range(fromFloor+1, self.length):
			value = self.values[i];
			if sum <= value:
				return i + (sum/value);
			sum -= value;

		# default: returns the largest possible "iTo":
		return values.length

	@lru_cache()
	def getCut(self, iFrom, value):
		"""/**
		 * Cut query.
		 * @param from where the piece starts.
		 * @param value what the piece value should be.
		 * @return where the piece should end.
		*/"""
		return self.invSum(iFrom, value)

	@lru_cache()
	def getValue(self, iFrom, iTo):
		"""/**
		 * Eval query
		 * @param from where the piece starts.
		 * @param to where the piece ends.
		 * @return the piece value.
		*/"""
		return self.sum(iFrom, iTo)

	@lru_cache()
	def getValueOfEntireCake(self):
		"""
	    >>> a = ValueFunction1D([1,2,3,4])
	    >>> a.getValueOfEntireCake()
	    10.0
		"""
		return self.sum(0, self.length)

	def getRelativeValue(self, iFrom, iTo):
		return self.getValue(iFrom,iTo) / self.getValuxxeOfEntireCake()



if __name__ == '__main__':
	import doctest
	doctest.testmod()
