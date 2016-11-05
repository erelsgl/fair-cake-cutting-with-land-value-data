/**
 * Run the Even-Paz algorithm on land value data.
 * Produce plots of the results using gnuplot.
 *
 * @author Erel Segal-Halevi, Gabi Burabia (gabi3b)
 * @since 2016-11
 */

import numpy as np
import utils.cakepartitions as cakepartitionsUtil
from utils import *

np.random.seed(1)

LAND_SIZE = 1000;
VALUE_PER_CELL = 100;
DATA_FILE_NAME ='data/newzealand_forests_npv_4q.1d.json'

meanValues = ValueFunction1D.fromJson(DATA_FILE_NAME);
print("cells in land: "+meanValues.length);

def calculate_results(aggregationType):
    if aggregationType == AggregationType.NumberOfAgents:
        for numOfAgents in NUMBER_OF_AGENTS:
            print("\n"+str(numOfAgents)+" agents")
    		var resultsFileName = "results/evenpaz-agents-"+numOfAgents+".dat";
    		var resultsFile = fs.createWriteStream(resultsFileName);

            agentsWithIdenticalValueFunctions = map(Agent, meanValues.noisyValuesArray(0, null, numOfAgents));
            identicalPartition = proportionalDivisionEvenPaz(agentsWithIdenticalValueFunctions); # returns a list of AllocatedPiece1D

            for noiseProportion in NOISE_PROPORTION:
    			print("\t"+str(noiseProportion)+" noise");
    			calculateSingleDatapoint(numOfAgents,noiseProportion,resultsFile);
    		resultsFile.end();
    		rungnuplot("main.gnuplot", "filename='"+resultsFileName+"'; xcolumn=3; xlabel='amplitude of deviation in utilities'", /*dry-run=*/!AUTOMATICALLY_RUN_GNUPLOT);

    elif aggregationType == AggregationType.Noise:
         for noise in NOISE_PROPORTION:
            print("\n"+str(noise)+" noise")
    		var resultsFileName = "results/evenpaz-noise-"+noiseProportion+".dat";
    		var resultsFile = fs.createWriteStream(resultsFileName);
            for numOfAgents in NUMBER_OF_AGENTS:
    			print("\t"+str(numOfAgents)+" agents");

                agentsWithIdenticalValueFunctions = map(Agent, meanValues.noisyValuesArray(0, null, numOfAgents));
                identicalPartition = proportionalDivisionEvenPaz(agentsWithIdenticalValueFunctions); # returns a list of AllocatedPiece1D

    			calculateSingleDatapoint(numOfAgents,noiseProportion,resultsFile);

    		resultsFile.end();
    		rungnuplot("main.gnuplot", "filename='"+resultsFileName+"'; xcolumn=2; xlabel='log num of people'", /*dry-run=*/!AUTOMATICALLY_RUN_GNUPLOT);
    	}
    else:
        raise Exception("Aggregation Type '%s' is not supported" % aggregationType)

def calculateSingleDatapoint(numOfAgents,noiseProportion,resultsFile):
	for iExperiment in range(EXPERIMENTS_PER_CELL):
        makeSingleExperiment(numOfAgents,noiseProportion,resultsFile)

def makeSingleExperiment(numOfAgents,noiseProportion,resultsFile):
    agents = map(Agent, meanValues.noisyValuesArray(noiseProportion, null, numOfAgents));

    partition = proportionalDivisionEvenPaz(agents); # returns a list of AllocatedPiece1D
    relativeValues = map(partition, lambda piece: piece.getRelativeValue())
    egalitarianValue = min(relativeValues)
    egalitarianGain = egalitarianValue*numOfAgents - 1;
    if (egalitarianGain<-0.001) raise ValueError("In proportional division, normalized egalitarian gain must be at least 0; got "+egalitarianGain);

    utilitarianValue = sum(relativeValues)
    utilitarianGain = utilitarianValue-1;
    if (utilitarianGain<-0.001) throw new Error("In proportional division, utilitarian gain must be at least 0; got "+utilitarianGain);

    mostEnviousAgent = max(partition, lambda piece: piece.largestEnvy(partition))
    largestEnvy = mostEnviousAgent.largestEnvy(partition)

    var identicalPartitionWithDifferentAgents = _.zip(valueFunctions,identicalPartition).map(function(pair) {
    	return new AllocatedPiece1D(pair[0], pair[1].from, pair[1].to);
    });
    var egalitarianGainIPWDA = cakepartitionsUtil.normalizedEgalitarianValue(identicalPartitionWithDifferentAgents)-1;
    var utilitarianGainIPWDA = cakepartitionsUtil.utilitarianValue(identicalPartitionWithDifferentAgents)-1;
    var envyIPWDA = cakepartitionsUtil.largestEnvy(identicalPartitionWithDifferentAgents);

    var data = numOfAgents+"\t"+np.log2(numOfAgents)+"\t"+noiseProportion+"\t"+
    	egalitarianGain+"\t"+utilitarianGain+"\t"+envy+"\t"+
    	egalitarianGainIPWDA+"\t"+utilitarianGainIPWDA+"\t"+envyIPWDA;
    resultsFile.write(data+"\n");



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
