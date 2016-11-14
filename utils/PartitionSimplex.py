# utils for drawing the partition simplex

def partitionSimplex(valueFunction, fractionIncrement):
	var length = valueFunction.length
	lengthIncrement = fractionIncrement * length
	for cut1 in range(0,length,lengthIncrement):
		for cut2 in range(cut1,length,lengthIncrement):
			
