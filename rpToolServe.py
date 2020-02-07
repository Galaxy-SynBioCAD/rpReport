#!/usr/bin/env python3

import tempfile
import os
import sys
import csv
import tarfile
import glob

import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api
import tempfile

sys.path.insert(0, '/home/')
import rpSBML
import rpTool



## run using HDD 3X less than the above function
#
#
def runReport_hdd(inputTar, csvfi, pathway_id='rp_pathway'):
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
    with open(csvfi_path, 'wb') as infi:
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


#######################################################
############## REST ###################################
#######################################################


app = Flask(__name__)
api = Api(app)


def stamp(data, status=1):
    appinfo = {'app': 'rpGlobalScore', 'version': '1.0',
               'author': 'Melchior du Lac',
               'organization': 'BRS',
               'time': datetime.now().isoformat(),
               'status': status}
    out = appinfo.copy()
    out['data'] = data
    return out


class RestApp(Resource):
    """ REST App."""
    def post(self):
        return jsonify(stamp(None))
    def get(self):
        return jsonify(stamp(None))


class RestQuery(Resource):
    """ REST interface that generates the Design.
        Avoid returning numpy or pandas object in
        order to keep the client lighter.
    """
    def post(self):
        inputTar = request.files['inputTar']
        csvfi = request.files['csvfi']
        params = json.load(request.files['data'])
        #### MEM ####
        #### HDD ####
        #weight_rp_steps, weight_fba, weight_thermo, pathway_id
        runReport_hdd(inputTar, csvfi, str(athway_id))
        #######################
        return send_file(csvfi, as_attachment=True, attachment_filename='rpReport.csv', mimetype='application/csv')


api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
