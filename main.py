"""
 * @author Erel Segal-Halevi, Gabi Burabia (gabi3b)
 * @since 2016-11
"""

import numpy as np
import matplotlib.pyplot as pyplot
from utils import *

np.random.seed(1)

LAND_SIZE = 1000;
VALUE_PER_CELL = 100;
DATA_FILE_NAME ='data/newzealand_forests_npv_4q.1d.json'

meanValues = ValueFunction1D.fromJson(DATA_FILE_NAME);
print("cells in land: "+meanValues.length);

algEvenPaz = AlgorithmEvenPaz1D()
algAssessor = AlgorithmAssessor1D(meanValues)

def calculate_results(aggregationType):
	if aggregationType == AggregationType.NumberOfAgents:
		for numOfAgents in NUMBER_OF_AGENTS:
			print("\n"+str(numOfAgents)+" agents")
			results = []
			for noiseProportion in NOISE_PROPORTION:
				print("\t"+str(noiseProportion)+" noise")
				results += calculateSingleDatapoint(numOfAgents,noiseProportion)
			plotResults(results, xAxisName = "noiseProportion")
			#rungnuplot("main.gnuplot", "filename='"+resultsFileName+"'; xcolumn=3; xlabel='amplitude of deviation in utilities'", /*dry-run=*/!AUTOMATICALLY_RUN_GNUPLOT);

	elif aggregationType == AggregationType.Noise:
		for noise in NOISE_PROPORTION:
			print("\n"+str(noise)+" noise")
			results = []
			for numOfAgents in NUMBER_OF_AGENTS:
				print("\t"+str(numOfAgents)+" agents");
				results += calculateSingleDatapoint(numOfAgents,noiseProportion,resultsFile);
			plotResults(results, xAxisName = "numOfAgents")
			#rungnuplot("main.gnuplot", "filename='"+resultsFileName+"'; xcolumn=2; xlabel='log num of people'", /*dry-run=*/!AUTOMATICALLY_RUN_GNUPLOT);
	else:
		raise Exception("Aggregation Type '%s' is not supported" % aggregationType)

def calculateSingleDatapoint(numOfAgents,noiseProportion):
	results = []
	for iExperiment in range(EXPERIMENTS_PER_CELL):
		results.append(makeSingleExperiment(algEvenPaz, numOfAgents,noiseProportion))
	return results

def makeSingleExperiment(algorithm, numOfAgents,noiseProportion):
	agents = map(Agent, meanValues.noisyValuesArray(noiseProportion, None, numOfAgents));

	partition = algorithm.run(agents) # returns a list of AllocatedPiece1D
	relativeValues = map(partition, lambda piece: piece.getRelativeValue())
	egalitarianValue = min(relativeValues)
	egalitarianGain = egalitarianValue*numOfAgents - 1;
	if (egalitarianGain<-0.001): raise ValueError("In proportional division, normalized egalitarian gain must be at least 0; got "+egalitarianGain);

	utilitarianValue = sum(relativeValues)
	utilitarianGain = utilitarianValue-1;
	if (utilitarianGain<-0.001): raise ValueError("In proportional division, utilitarian gain must be at least 0; got "+utilitarianGain);

	mostEnviousAgent = max(partition, lambda piece: piece.largestEnvy(partition))
	largestEnvy = mostEnviousAgent.largestEnvy(partition)

	return {
		"numOfAgents": numOfAgents,
		"noiseProportion": noiseProportion,
		"egalitarianGain": egalitarianGain,
		"utilitarianGain": utilitarianGain,
		"largestEnvy": largestEnvy,
		}

def plotResults(results, xAxisName):
	xAxis = map(lambda result: result[xAxisName], results)
	print(xAxis)

if __name__ == '__main__':
	print (os.path.realpath(__file__))

	EXPERIMENTS_PER_CELL = 10

	NOISE_PROPORTION = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
	NUMBER_OF_AGENTS = [32]
	calculate_results(AggregationType.NumberOfAgents)

#    NOISE_PROPORTION = [0.2,0.8]
#    NUMBER_OF_AGENTS = [2,4,8,16,32,64,128]
#    calculate_results(AggregationType.Noise)

	print('completed.')
