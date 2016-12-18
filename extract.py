#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os, json
import lxml.html

from logger import logger

class Extractor(object):
    '''
        extract something from content
    '''
    def __init__(self, xpath_dic=None):
        logger.info("extractor init OK")
    
    def xpath_extract(self, cont, xpath):
        if type(cont) == unicode:
            data = lxml.html.fromstring(cont)
        else:
            data = cont
        
        res = []
        if not hasattr(data, 'xpath'):
            logger.error("failed to xpath parse for no xpath method in this object")
            return res

        res = data.xpath(xpath)
        return res

    def json_extractor(self, cont, ):
        pass
