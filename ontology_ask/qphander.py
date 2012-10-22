#! /usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import base64
from xmlhandler import xmlhandler

############
# get query/parse result from backend interface
# 
################


class qphandler:
    def __init__(self):
        pass

    def __get_query_rlt(self,url,case):
        queryurl = self.__struct_query_str(url,case)
        data = urllib2.urlopen(queryurl).read()
        uidata = json.loads(data)['results'][1]['uidata']
        self.qdata = json.loads(data)['results'][1]['qdata']
        self.qid = json.loads(base64.b64decode(uidata))['qid']

    def get_parse_rlt(self,queryurl,parseurl,case):
        """
        return result data length and qid in dict
        else return null
        """
        try:
            self.__get_query_rlt(queryurl,case)
            req = self.__struct_parse_str(parseurl)
            data = urllib2.urlopen(req).read()
            rltlength = xmlhandler().parse_rltitem(data)
            return {'rlt':rltlength,'qid':self.qid}
        except Exception:
            return {}
    

    def __struct_parse_str(self,parseurl):
        """
        generate parse request
        """
        headers = {"Content-type":"text/plain"}
        req = urllib2.Request(parseurl + '/solr/queans/query/?wt=xml&indent=on',data=self.qdata, headers = headers)
        return req

    def __struct_query_str(self,url,case):
        """
        generate query url
        """
        return url + '/solr/queans/parse/?q=%s&wt=json&indent=on' %(urllib2.quote(case))

if __name__ == '__main__':
    case = 'pe>5'
    queryurl = 'http://192.168.23.52:9998'
    parseurl = 'http://192.168.23.52:9999'
    ih = qphandler()
    ih.get_parse_rlt(queryurl,parseurl,case)
    

