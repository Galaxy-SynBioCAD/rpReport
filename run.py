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

##
#
#
def main(inputfile,
         input_format,
         output,
         pathway_id='rp_pathway'):
    docker_client = docker.from_env()
    image_str = 'brsynth/rpreport-standalone:v1'
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
        if not 'ERROR' in err_str:
        	shutil.copy(tmpOutputFolder+'/output.dat', output)
        else:
            print(err_str)
        container.remove()



##
#
#
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
