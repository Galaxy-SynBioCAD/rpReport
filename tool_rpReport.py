#!/usr/bin/python

import tempfile
import glob
import os
import tarfile
import argparse

import sys
sys.path.insert(0, '/home/')

import rpToolServe


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Write CSV report')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-pathway_id', type=str)
    params = parser.parse_args()
    #sbml read the different mode
    if params.input_format=='tar':
        rpToolServe.runReport_hdd(params.input, params.output, params.pathway_id)
    elif params.input_format=='sbml':
        #make the tar.xz 
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            inputTar = tmpOutputFolder+'/tmp_input.tar.xz'
            with tarfile.open(inputTar, mode='w:xz') as tf:
                info = tarfile.TarInfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                info.size = os.path.getsize(params.input)
                tf.addfile(tarinfo=info, fileobj=open(params.input, 'rb'))
            rpToolServe.runReport_hdd(inputTar, params.output, params.pathway_id)
    else:
        logging.error('Cannot identify the input/output format: '+str(params.input_format))
