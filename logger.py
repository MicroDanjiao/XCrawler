#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging, logging.handlers

def init_log(log_file=None, level=logging.DEBUG, name="xcrawler"):
    if log_file:
        handler = logging.handlers.RotatingFileHandler(log_file, maxBytes = 1024*1024*500, backupCount = 5)   
    else:
        handler = logging.StreamHandler()
    fmt = '%(asctime)s-%(filename)s:%(lineno)s[%(levelname)s]: %(message)s'
    formatter = logging.Formatter(fmt)   # 实例化formatter  
    handler.setFormatter(formatter)      # 为handler添加formatter  
 
    logger = logging.getLogger(name)    # 获取名为lda的logger  
    logger.addHandler(handler)           # 为logger添加handler  
    logger.setLevel(level)
    return logger

logger = init_log()

