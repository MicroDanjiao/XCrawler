#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os, json
import ConfigParser 

from logger import logger

class Config(object):
    '''
        parse config file
    '''
    def __init__(self, cfg_file, root="root"):
        self.config = ConfigParser.ConfigParser()
        self.config.read(cfg_file)
        self.root = root
        
        self.root_required_key = ['seeds', 'action']
        self.node_required_key = ['name', 'type', 'value', 'fetch', 'action']
        self.type_option = ['xpath', 'json']

    def get_parse_tree(self):
        #try:
            kvs = self.config.items(self.root)
            self.tree = dict(kvs)
            for key in self.root_required_key:
                if key not in self.tree:
                    raise Exception("%s is requred in %s" %(key, self.root))
            self.tree['seeds'] = self.tree['seeds'].split(',')
            action = []
            for act in self.tree['action'].split(','):
                if act == "save":
                    raise Exception("root node's action can not be save!")
                else:
                    action.append(self.parse_node(act))
            self.tree['action'] = action
            logger.info("parse config file OK!")
            return self.tree           
        #except Exception as e:
        #    logger.error("parse config file error:\n%s" %e)
        #    sys.exit()

    def parse_node(self, act):
        kvs = self.config.items(act)
        tmpdic = dict(kvs)
        for key in self.node_required_key:
            if key not in tmpdic:
                raise Exception("%s is requred in %s" %(key, act))
        action = []
        for act in tmpdic['action'].split(','):
             if act == "save":
                action.append("save")
             else:
                action.append(self.parse_node(act))
        if tmpdic['type'] not in self.type_option:
            raise Exception("%s of node type is not supported" %tmpdic['type'])

        tmpdic['fetch'] = int(tmpdic['fetch'])
        tmpdic['action'] = action
        return tmpdic

if __name__ == '__main__':
    config = Config('crawler.cfg')
    tree = config.get_parse_tree()
    print json.dumps(tree, ensure_ascii=False, indent=4).encode("u8")
    


