#!/usr/bin/env python3

import tempfile
import os
import sys
import csv
import tarfile
import glob

sys.path.insert(0, '/home/')
import rpSBML
import rpTool



## run using HDD 3X less than the above function
#
#
def runReport_hdd(inputTar, csvfi_path, pathway_id='rp_pathway'):
    header = ['Pathway Name', 
              'Reaction', 
              'Global Score', 
              'Rule ID',
              'Reaction Rule',
              'Rule Score',
              'dfG_prime_o',
              'dfG_prime_m',
              'dfG_uncert',
              'Normalised dfG_prime_o',
              'Normalised dfG_prime_m',
              'Normalised dfG_uncert',
              'FBA',
              'FBA Flux',
              'FBA Normalised Flux',
              'UniProt',
              'Selenzyme Score']
    with open(csvfi_path, 'w') as infi:
        csvfi = csv.writer(infi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvfi.writerow(header)
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            with tempfile.TemporaryDirectory() as tmpInputFolder:
                tar = tarfile.open(fileobj=inputTar, mode='r:xz')
                tar.extractall(path=tmpInputFolder)
                tar.close()
                for sbml_path in glob.glob(tmpInputFolder+'/*'):
                    fileName = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '').replace('.rpsbml', '')
                    rpsbml = rpSBML.rpSBML(fileName)
                    rpsbml.readSBML(sbml_path)
                    rpTool.writeLine(rpsbml, csvfi, pathway_id)


##
#
#
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Given an SBML, extract the reaction rules and pass them to Selenzyme REST service and write the results to the SBML')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-report_csv', type=str)
    parser.add_argument('-pathway_id', type=str)
    params = parser.parse_args()
    #sbml read the different mode
    if params.input_format=='tar':
        runReport_hdd(params.input, params.report_csv, params.pathway_id)
    elif params.input_format=='sbml':
        #make the tar.xz 
        with tempfile.TemporaryDirectory() as tmpOutputFolder:
            inputTar = tmpOutputFolder+'/tmp_input.tar.xz'
            with tarfile.open(inputTar, mode='w:xz') as tf:
                info = tarfile.TarInfo('single.rpsbml.xml') #need to change the name since galaxy creates .dat files
                info.size = os.path.getsize(params.input)
                tf.addfile(tarinfo=info, fileobj=open(params.input, 'rb'))
            runReport_hdd(inputTar, params.report_csv, params.pathway_id)
    else:
        logging.error('Cannot identify the input/output format: '+str(params.input_format))
    exit(0)
