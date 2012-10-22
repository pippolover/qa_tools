#! /usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree

class xmlhandler:
    def __init__(self):
        pass


    def parse_rltitem(self,xmlstr):
        """
        get 股票代码 data column length
        if data column exist, result will not empty
        """
        length = 0
        if xmlstr:
            try:
                xmldoc = etree.fromstring(xmlstr)
                rlt = xmldoc.xpath('//arr/lst/str[@name="data"]')[0]
                if rlt.text:
                    length = len(rlt.text)
            except Exception,e:
                print e
        return length

