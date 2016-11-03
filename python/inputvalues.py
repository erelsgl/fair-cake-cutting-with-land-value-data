"""
/**
 * Utility functions for reading input values.
 *
 * @author Erel Segal-Halevi
 * @since 2016-11
 */
"""
import json
import numpy as np

def valuesFromFile(filename):
    with open(filename) as data_file:
        return json.load(data_file)

def noisyValues(mean_values, noise_proportion, normalized_sum):
    """/**
	 * @param meanValues array
	 * @param noiseProportion a number in [0,1]
	 * @return an array of values of the same size as meanValues; to each value, the function adds a random noise, drawn uniformly from [-noiseRatio,noiseRatio]*value
     * @author Gabi Burabia
	 */"""
    aggregated_sum = 0
    values = [0] * len(mean_values)
    for i in range(len(mean_values)):
        noise = (2*np.random()-1)*noise_proportion
        newVal = mean_values[i]*(1+noise)
        newVal = max(0, newVal)
        aggregated_sum += newVal
        values[i] = newVal
    if aggregated_sum > 0 and normalized_sum is not None and normalized_sum > 0:
        normalization_factor = normalized_sum / aggregated_sum
        for i in range(len(values)):
            values[i] *= normalization_factor
    return values


def noisyValuesArray(mean_values, noise_proportion, normalized_sum, num_of_agents):
    values = []
    for i in range(num_of_agents):
        values.append(noisyValues(mean_values, noise_proportion, normalized_sum))
    return values
