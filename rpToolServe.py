import tempfile
import os
import sys
import csv
import tarfile
import glob
import logging

logging.basicConfig(
    #level=logging.DEBUG,
    level=logging.WARNING,
    #level=logging.ERROR,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
)

import rpSBML
import rpTool

def runReport_hdd(inputTar, csvfi_path, pathway_id='rp_pathway'):
    """Generate the csv report file

    :param inputTar: Input TAR file
    :param csvfi_path: Path to the output report file
    :param pathway_id: The id of the pathway (Default: rp_pathway)

    :type inputTar: str
    :type csvfi_path: str
    :type pathway_id: str

    :rtype: bool
    :return: The success or failure of the function
    """
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
        with tempfile.TemporaryDirectory() as tmpInputFolder:
            tar = tarfile.open(inputTar, mode='r')
            tar.extractall(path=tmpInputFolder)
            tar.close()
            if len(glob.glob(tmpInputFolder+'/*'))==0:
                logging.error('Input file is empty')
                return False
            for sbml_path in glob.glob(tmpInputFolder+'/*'):
                fileName = sbml_path.split('/')[-1].replace('.sbml', '').replace('.xml', '').replace('.rpsbml', '')
                rpsbml = rpSBML.rpSBML(fileName)
                rpsbml.readSBML(sbml_path)
                rpTool.writeLine(rpsbml, csvfi, pathway_id)
    return True
