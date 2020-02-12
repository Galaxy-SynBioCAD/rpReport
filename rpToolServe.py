#!/usr/bin/python

import tempfile
import os
import sys
import csv
import tarfile
import glob
import io
import tempfile
import logging

import json
from datetime import datetime
from flask import Flask, request, jsonify, send_file, abort
from flask_restful import Resource, Api

sys.path.insert(0, '/home/')
import rpSBML
import rpTool



## run using HDD 3X less than the above function
#
#
def runReport_hdd(input_tar, output_bytes, pathway_id='rp_pathway'):
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
    csvfi = csv.writer(output_bytes, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvfi.writerow(header)
    #csvfi.writerow([i.encode('utf-8') for i in header])
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        with tempfile.TemporaryDirectory() as tmpInputFolder:
            tar = tarfile.open(fileobj=input_tar, mode='r:xz')
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
        input_tar = request.files['input_tar']
        params = json.load(request.files['data'])
        output_csv = io.StringIO()
        #output_csv = io.BytesIO()
        #### MEM ####
        #### HDD ####
        #weight_rp_steps, weight_fba, weight_thermo, pathway_id
        runReport_hdd(input_tar, output_csv, str(params['pathway_id']))
        ######## IMPORTANT #########
        #output_csv.seek(0)
        mem = io.BytesIO()
        mem.write(output_csv.getvalue().encode('utf-8'))
        mem.seek(0)
        output_csv.close()
        ############################
        return send_file(mem, as_attachment=True, attachment_filename='rpReport.csv', mimetype='application/csv')


api.add_resource(RestApp, '/REST')
api.add_resource(RestQuery, '/REST/Query')


if __name__== "__main__":
    app.run(host="0.0.0.0", port=8888, debug=False, threaded=True)
