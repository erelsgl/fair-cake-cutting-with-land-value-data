fair-division
=============

Algorithms and experiments related to fair division. In particular, fair division of land.

Prerequisites
-------------
To run the program you need [Node.js](http://nodejs.org/).

To show the plots you need [gnuplut](http://www.gnuplot.info/), but the results are given in plain text format so you can probably use other plotting software. 

Installation
------------
Clone the repository, then run:

		npm install
		
Experiments
-----------	

Edit the main.js file and change the experiment details, i.e. the numbers of agents or the noise proportion.

Go to the fair-division folder and run: 

		node main.js

This will create some data files in the "results/" folder. 

On the console, you will see some gnuplot commands that you can use to plot the results, such as:

		gnuplot --persist  -e "filename='results/evenpaz-noise-0.2.dat'; xcolumn=1" main.gnuplot
 
Plots
-----	
The plots show the performance of the fair division algorithm, vs. the performance of the "objective" assessor division ("shamay").

Currently there are three performance measures: egalitarian social welfare, utilitarian social welfare, and envy.
