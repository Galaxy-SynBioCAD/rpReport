#!/usr/bin/env python3

import sys
import rpSBML
import logging


def getInfo(brs_dict, key):
    """Extract the required info from the BRSynth annotation

    :param brs_dict: The BRSynth dictionary
    :param key: The key to extract the info from 

    :type brs_dict: dict
    :type key: str

    :rtype: str
    :return: The extracted value
    """
    try:
        toRet = brs_dict[key]['value']
        if toRet=={}:
            return ''
        return str(toRet)
    except (KeyError, TypeError) as e:
        try:
            toRet = brs_dict[key]
            if toRet=={}:
                return ''
            return str(toRet)
        except (KeyError, TypeError) as e:
            return ''


def writeLine(rpsbml, csvfi, pathway_id='rp_pathway'):
    """Write the lines in the report from a rpSBML file

    :param rpsbml: The input rpSBML object
    :param csvfi: The csv output file
    :param pathway_id: The id of the heterologous pathway

    :type rpsbml: rpSBML
    :type csvfi: csv.writer
    :type pathway_id: str

    :rtype: None
    :return: None
    """
    #loop through all the groups reactions
    groups = rpsbml.model.getPlugin('groups')
    rp_pathway = groups.getGroup(pathway_id)
    path_brs_dict = rpsbml.readBRSYNTHAnnotation(rp_pathway.getAnnotation())
    logging.debug('path_brs_dict: '+str(path_brs_dict))
    ### pathway
    to_write = [rpsbml.model.getId(),
                'pathway',
                getInfo(path_brs_dict, 'global_score'),
                getInfo(path_brs_dict, 'rule_id'),
                getInfo(path_brs_dict, 'smiles'),
                getInfo(path_brs_dict, 'rule_score'),
                getInfo(path_brs_dict, 'dfG_prime_o'),
                getInfo(path_brs_dict, 'dfG_prime_m'),
                getInfo(path_brs_dict, 'dfG_uncert'),
                getInfo(path_brs_dict, 'norm_dfG_prime_o'),
                getInfo(path_brs_dict, 'norm_dfG_prime_m'),
                getInfo(path_brs_dict, 'norm_dfG_uncert')]
    to_write.append(';'.join([str(i) for i in list(path_brs_dict.keys()) if i[:4]=='fba_']))
    to_write.append(';'.join([str(path_brs_dict[i]['value']) for i in list(path_brs_dict.keys()) if i[:4]=='fba_']))
    to_write.append(';'.join([str(path_brs_dict[i]['value']) for i in list(path_brs_dict.keys()) if i[:8]=='norm_fba']))
    #to_write.append(';'.join([str(path_brs_dict[i]) for i in list(path_brs_dict.keys()) if i[:8]=='norm_obj']))
    try:
        to_write.append(';'.join([str(i) for i in list(path_brs_dict['selenzyme'].keys())]))
        to_write.append(';'.join([str(path_brs_dict['selenzyme'][i]) for i in list(path_brs_dict['selenzyme'].keys())]))
    except (KeyError, AttributeError) as e:
        to_write.append('')
        to_write.append('')
    csvfi.writerow(to_write)
    ### reaction
    for member in rp_pathway.getListOfMembers():
        reaction = rpsbml.model.getReaction(member.getIdRef())
        reac_brs_dict = rpsbml.readBRSYNTHAnnotation(reaction.getAnnotation())
        to_write = [rpsbml.model.getId(),
                    reaction.getId(),
                    getInfo(reac_brs_dict, 'global_score'),
                    getInfo(reac_brs_dict, 'rule_id'),
                    getInfo(reac_brs_dict, 'smiles'),
                    getInfo(reac_brs_dict, 'rule_score'),
                    getInfo(reac_brs_dict, 'dfG_prime_o'),
                    getInfo(reac_brs_dict, 'dfG_prime_m'),
                    getInfo(reac_brs_dict, 'dfG_uncert'),
                    getInfo(reac_brs_dict, 'norm_dfG_prime_o'),
                    getInfo(reac_brs_dict, 'norm_dfG_prime_m'),
                    getInfo(reac_brs_dict, 'norm_dfG_uncert')]
        to_write.append(';'.join([str(i) for i in reac_brs_dict.keys() if i[:4]=='fba_']))
        to_write.append(';'.join([str(reac_brs_dict[i]['value']) for i in list(reac_brs_dict.keys()) if i[:4]=='fba_']))
        to_write.append(';'.join([str(reac_brs_dict[i]['value']) for i in reac_brs_dict.keys() if i[:8]=='norm_fba']))
        #to_write.append(';'.join([str(reac_brs_dict[i]) for i in reac_brs_dict.keys() if i[:8]=='norm_fba']))
        try:
            to_write.append(';'.join([str(i) for i in reac_brs_dict['selenzyme'].keys()]))
            to_write.append(';'.join([str(reac_brs_dict['selenzyme'][i]) for i in reac_brs_dict['selenzyme'].keys()]))
        except (KeyError, AttributeError) as e:
            to_write.append('')
            to_write.append('')
        csvfi.writerow(to_write)
