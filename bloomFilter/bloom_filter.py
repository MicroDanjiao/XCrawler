#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys, os 
from ctypes import *

sys.path.append("..")
from logger import logger

class BloomFilter(object):
    '''
        wrapper of c-implementation bloom filter
        if this do not work, maybe could use pybloom package
    '''
    def __init__(self, size=250000):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        libpath = os.path.join(cur_dir, "c_code/bloom_filter.so")
        self.lib = cdll.LoadLibrary(libpath)
        self.bf = self.lib.bloom_create_tmp(size)
        logger.info("init bloom filter OK!")

    def add(self, s):
        return self.lib.bloom_add(self.bf, s)

    def check(self, s):
        return self.lib.bloom_check(self.bf, s)

    def destroy(self):
        self.lib.bloom_destroy(self.bf)


    
if __name__ == '__main__':
    bf = BloomFilter()
    s1 = "www.baidu.com"
    s2 = "www.163.com"
    print bf.add("www.baidu.com")
    print bf.check("www.baidu.com")
    print bf.check(s1)
    print bf.add(s1)
    print bf.check(s1)
    bf.destroy()

