import unittest
import os
import sys
import csv
import hashlib
import tempfile

sys.path.insert(0, '..')

import rpTool
#WARNING: Need to copy a version of rpSBML locally
import rpSBML

class TestRPTool(unittest.TestCase):

    """
    @classmethod
    def setUpClass(self):
    """

    def test_writeLine(self):
        with tempfile.TemporaryDirectory() as tmp_output_folder:
            with open(os.path.join(tmp_output_folder, 'tmp.csv'), 'w') as infi:
                csvfi = csv.writer(infi, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                rpsbml = rpSBML.rpSBML('test', path=os.path.join('data', 'rpsbml.xml'))
                rpTool.writeLine(rpsbml, csvfi)
            self.assertEqual(hashlib.md5(open(os.path.join(tmp_output_folder, 'tmp.csv'), 'rb').read()).hexdigest(), '71c79991dc83308cc76c4ffc6cc91e93')
                
