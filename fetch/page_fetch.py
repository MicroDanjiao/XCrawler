#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys, os, json
import urllib
import urllib2
import StringIO
import gzip
import cookielib
from urlparse import urljoin
from encoding import *

sys.path.append('..')
from logger import logger

class PageFetch(object):
    '''
        my_crawler: crawl something
    '''
    def __init__(self, cookie_file="cookies"):
        
        self.headers = {
            'Accept':'text/html',
            'Accept-Language':' zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0' ,
            'Connection':'keep-alive' ,
            'Upgrade-Insecure-Requests':'1' ,
            'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        }
        self.cookie_file = cookie_file
        logger.info('init page fetcher OK')

    def fetch(self, url, postdata=None, timeout=10, load_cookie=False, save_cookie=False,
                referer=None, accept=None):
        '''
            fecth the html using urllib2
        '''
        try:
            #open request
            logger.info("fetch url %s" %url)
            # proc headers
            headers = dict(self.headers)
            if accept:
                headers['Accept'] = accept
            if referer:
                headers['Referer'] = referer
            # proc request
            req = urllib2.Request(url, headers=headers)
            if postdata:
                postdata = self.proc_postdata(postdata)
                req.add_data(urllib.urlencode(postdata))
            
            # cookie related
            if load_cookie or save_cookie:
                cookie = cookielib.MozillaCookieJar()
                if load_cookie:
                    cookie.load(self.cookie_file, ignore_discard=True, ignore_expires=True)
                opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
                response = opener.open(req, timeout=timeout)
            else:
                response = urllib2.urlopen(req, timeout=timeout)
        
            # fetch response
            url = response.geturl()
            if response.code != 200:
                logger.info("fetch failed, url:%s, code:%s" %(url, response.code))
                return (url, None)

            if save_cookie:
                cookie.save(self.cookie_file, ignore_discard=True, ignore_expires=True)

            headers = dict(response.headers)
            res = response.read()
            # check compression
            if 'content-encoding' in headers:
                if 'gzip' in headers['content-encoding']:
                    res = self.gzdecode(res)

            # encoding parse
            try:
                charset = res.headers['Content-Type'].split('charset=')[1].split(';')[0].lower()
                content = unicode(res, charset, 'ignore')                    
            except:            
                encode, content = html_to_unicode(None, res) 
            return (url, content)

        except Exception as e:
            logger.error("fetch %s Exception:\n%s" %(url, e))
            return (url, None)

    def gzdecode(self, data) :  
        gziper = gzip.GzipFile(fileobj=StringIO.StringIO(data),mode="r")    
        return gziper.read()

    def proc_postdata(self, data):
        if type(data) == dict:
            return data
        try:
            ds = data.split('&')
            ds = [d.split('=') for d in ds]
            data = dict(ds)
            return data
        except Exception as e:
            logger.error("parse post data error,\n%s" %e)
            return {} 
        
if __name__ == '__main__':
    crawler = PageFetch()
    page = crawler.fetch('http://www.baidu.com', load_cookie=True)
    
    #page = crawler.fetch('http://www.meet99.com/lvyou-OSAKA.html')
    #print page


