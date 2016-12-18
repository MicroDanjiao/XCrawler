#!/usr/bin/env 
# -*- coding:utf-8 -*-

import sys, os, json
import lxml.html

from logger import logger
from fetch.page_fetch import PageFetch
from extract import Extractor
from config_parser import Config
from urlparse import urljoin
from bloomFilter.bloom_filter import BloomFilter

class XCrawler(object):
    def __init__(self, config_file, outfile=None):
        self.fetcher = PageFetch()
        self.extractor = Extractor()
        self.tree = Config(config_file).get_parse_tree()
        self.outfile = outfile
        if outfile:
            self.out = open(outfile, 'w')
        else:
            self.out = sys.stdout
        self.bf = BloomFilter(size=25000)
        logger.info("init crawler OK!")

    def start(self):
        for seed in self.tree['seeds']:
            logger.info("start to crawl seed %s" %seed)
            result = {}
            for act in self.tree['action']:
                name, value = self._do_action(act, seed, None)
                result[name] = value
            logger.info("finish process seed %s" % seed)
            print >> self.out, json.dumps(result, ensure_ascii=False, indent=4).encode("u8")

    def _do_action(self, node, cont, parent_url):
        ''' do some actions'''
        if type(node) != dict:
            raise Exception("parse node must be dict!")

        cont_tree = None
        values = []
        url = None
        
        if node['fetch'] == 1:
            url = cont
            if parent_url:
                url = urljoin(parent_url, url)

            if self.bf.check(url):
                logger.warn("url %s is crawled" %url)
                return node['name'], values

            url, cont = self.fetcher.fetch(url)
            if not cont:
                logger.error("fetch url %s failed" %url) 
                return node['name'], values

            self.bf.add(url)
            cont_tree = lxml.html.fromstring(cont)         

        results = self._do_extract(node['type'], cont, node['value'], cont_tree)
        for res in results:
            for act in node['action']:
                if act == "save":
                    values.append(res)
                else:
                    if not url:
                        url = parent_url
                    name, value = self._do_action(act, res, parent_url=url)
                    values.append({name:value})
        return node['name'], values

    def _do_extract(self, ext_type, cont, value, cont_tree=None):
        ''' do some extractions '''
        if ext_type == "xpath":
            if cont_tree is not None:
                cont = cont_tree
            results = self.extractor.xpath_extract(cont, value)
        else:
            results = []
        return results

    def close(self):
        if self.outfile:
            self.out.close()
        self.bf.destroy()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print >> sys.stderr, "Usage: %s <config_file>" % sys.argv[0]
    crawler = XCrawler(sys.argv[1])
    crawler.start()
    crawler.close()
