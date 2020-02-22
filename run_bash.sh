#!/bin/bash

docker run -v $1:/home/input_file.dat -v ${PWD}/results/:/home/results/ --rm brsynth/rpreport-standalone python /home/tool_rpReport.py -input /home/input_file.dat -input_format $2 -output /home/results/rpReport.csv -pathway_id rp_pathway

cp ${PWD}/results/rpReport.csv .
rm -r ${PWD}/results/
