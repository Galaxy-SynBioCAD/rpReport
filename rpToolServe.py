#!/usr/bin/python

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
