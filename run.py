#!/usr/bin/env python3
"""
Created on March 17 2020

@author: Melchior du Lac
@description: rpOptBioDes

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker
import glob


def main(inputfile,
         input_format,
         output,
         pathway_id='rp_pathway'):
    """Call the docker object to run and generate the report

    :param inputfile: The input file path
    :param input_format: The input file format (Valid Options: ['tar', 'sbml'])
    :param output: The output file path
    :param pathway_id: The id of the heterologous pathway (Default: 'rp_pathway')

    :type inputfile: str
    :type input_format: str
    :type output: str
    :type pathway_id: str

    :rtype: None
    :return: None
    """
    docker_client = docker.from_env()
    image_str = 'brsynth/rpreport-standalone:v2'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        if os.path.exists(inputfile):
            shutil.copy(inputfile, tmpOutputFolder+'/input.dat')
            command = ['python',
                       '/home/tool_rpReport.py',
                       '-input',
                       '/home/tmp_output/input.dat',
                       '-input_format',
                       str(input_format),
                       '-output',
                       '/home/tmp_output/output.dat',
                       '-pathway_id',
                       str(pathway_id)]
            container = docker_client.containers.run(image_str,
                                                     command,
                                                     detach=True,
                                                     stderr=True,
                                                     volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
            container.wait()
            err = container.logs(stdout=False, stderr=True)
            err_str = err.decode('utf-8')
            if 'ERROR' in err_str:
                print(err_str)
            elif 'WARNING' in err_str:
                print(err_str)
            if not os.path.exists(tmpOutputFolder+'/output.dat'):
                print('ERROR: Cannot find the output file: '+str(tmpOutputFolder+'/output.dat'))
            else:
                shutil.copy(tmpOutputFolder+'/output.dat', output)
            container.remove()
        else:
            logging.error('The input file does not seem to exist: '+str(inputfile))
            exit(1)



if __name__ == "__main__":
    parser = argparse.ArgumentParser('Generate CSV fold')
    parser.add_argument('-input', type=str)
    parser.add_argument('-input_format', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-pathway_id', type=str, default='rp_pathway')
    params = parser.parse_args()
    main(params.input,
         params.input_format,
         params.output,
         params.pathway_id)
