# -*- coding: utf-8 -*-
import urllib2
import json
from regressLogger import log
import cookielib

class webdataUtil:
    """
    get result data from web interface 
    source = data
    """
    def __init__(self):
        """
        build url opener with cookie file in case
        newbie helper showup
        """
        cj = cookielib.LWPCookieJar()
        cj.revert('cookie.txt')
        cjhandler=urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cjhandler)
        urllib2.install_opener(opener)

    def __struct_dict(self,dic):
        rlt = {}
        titlelist = dic.get('title')
        #title_opt = [self.__strip_title(title) for title in titlelist]
        #rlt['title'] = title_opt
        #print dic.get('result')
        try:
            for key,result in dic.get('result').items():
                stockcode = self.__strip_stockcode(key)
                tmp = {}
                for counter,item in enumerate(result):
                    tmp[self.__strip_title(titlelist[counter])] = item
                rlt[stockcode] = tmp
        except AttributeError,e:
            print e.message
            print'对不起，该query没有问答数据'
        return rlt

    def __strip_title(self,title):
        return title.split('<')[0].strip()


    def __strip_stockcode(self,stockcode):
        return stockcode.split('.')[0]

    def __build_cookie(self):
        cj = cookielib.CookieJar()
        cjhandler=urllib2.HTTPCookieProcessor(cj)
        opener = urllib2.build_opener(cjhandler)
        urllib2.install_opener(opener)

    def get_ontology_data(self,sentence):
        prefix = 'http://x.10jqka.com.cn/stockpick/search?w='
        #prefix = 'http://192.168.23.105/stockpick/search?w='
        query = prefix + urllib2.quote(sentence)+ "&source=data"
        try:
            data = urllib2.urlopen(query).read()
            #print data
        except (IOError,urllib2.HTTPError,urllib2.URLError),e:
            log.debug('case:' + sentence.decode('utf-8') + "catch http error")
        returndata = ""
        try:
            returndata = json.loads(data)
        except ValueError:
            log.debug(sentence.decode('utf-8') + "not return json data")
        except UnboundLocalError:
            log.debug(sentence.decode('utf-8') + "not return json data")
        return returndata

    def struct_web_data(self,dic,rdclient):
        """
        dic struct is:
            {stockcode:{title:value}}
        """
        dic_opt = {}
        for stockcode,item in dic.items():
            tmp = {}
            for title,value in item.items():
                #decode data get from redis as redis encoding is different
                title_opt = rdclient.get(title).decode('utf-8') if rdclient.get(title) else title
                tmp[title_opt] = value
            dic_opt[stockcode] = tmp
        return dic_opt

    def restruct_data(self,li):
        """restruct data from list
        to dict"""
        dic = {}
        for l in li:
            dic[l[0]] = l[1]
        return dic

if __name__ == '__main__':
    wd = webdataUtil()
    query = "昨天上榜的股票"
    print wd.get_ontology_data(query)
