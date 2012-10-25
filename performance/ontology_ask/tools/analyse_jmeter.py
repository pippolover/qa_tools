#! /usr/bin/env python
# -*- coding: utf-8 -*-
################################################################
# this script is to analysis jmeter logfile in None_GUI mode
# and get result as aggregate report
# @author: wuyiming@myhexin.com
# @2012/3/19
################################################################

from xml.etree import ElementTree
from datetime import datetime
import time
import pprint
import sys

class analyse_jmeter:
    def __init__(self,filename):
        self.filename = filename

    def read_file(self,filetype):
        if filetype == 'xml':
            root = ElementTree.parse(self.filename)
            sample_node = root.getiterator("httpSample")
        else:
            plainfile = file(self.filename,'r')
            sample_node = plainfile.read().split('\n')
        return sample_node
  
    def get_aggregate_report(self,sample_node):
        self.t_totle= []
        self.totle_time = 0
        self.totle = len(sample_node)
        self.succ_num = 0
        self.max_response_time = 0
        self.min_response_time = 100000000
        starttime = 133215051688900
        endtime = 0
        for node in sample_node:
            if node.attrib.has_key("t"):
                self.t_totle.append(int(node.attrib["t"]))
                self.totle_time += int(node.attrib["t"])
                if int(node.attrib["t"]) > self.max_response_time:
                    self.max_response_time = int(node.attrib["t"])
                if int(node.attrib["t"]) < self.min_response_time :
                    self.min_response_time = int(node.attrib["t"])
            if node.attrib["rc"] == '200':
                succ_num += 1
            if int(node.attrib["ts"]) < starttime:
                starttime = int(node.attrib["ts"])
            if int(node.attrib["ts"]) > endtime:
                endtime = int(node.attrib["ts"])

    def get_plain_aggregate_report(self,sample_node):
        """
        nodelist struct [timestamp,time_spend,sample_name,http_code,http_status,
            thread_group,return_type,assert_result]
        """
        self.t_totle= {}
        self.totle_time = 0
        self.totle = len(sample_node)
        self.succ_num = 0
        self.max_response_time = 0
        self.min_response_time = 100000000
        for node in sample_node:
            if node:
                nodelist = node.split(',') 
                sampler = nodelist[2]
                if not self.t_totle.has_key(nodelist[2]):
                    self.t_totle[sampler] = {}
                    self.t_totle[sampler]['fail_num'] = 0
                    self.t_totle[sampler]['sample'] = []
                    self.t_totle[sampler]['totle_time'] = 0
                    self.t_totle[sampler]['succ_num'] = 0
                    self.t_totle[sampler]['timestamp'] = []
                    self.t_totle[sampler]['assert_fails'] = 0
                    self.t_totle[sampler]['lt_200'] = 0
                    self.t_totle[sampler]['lt_500'] = 0
                    self.t_totle[sampler]['lt_1000'] = 0
                    self.t_totle[sampler]['gt_1000'] = 0
                if str(nodelist[3]) == '200':
                    if int(nodelist[1]) <= 200:
                        self.t_totle[sampler]['lt_200'] += 1
                    if int(nodelist[1]) >200 and int(nodelist[1]) <= 500:
                        self.t_totle[sampler]['lt_500'] += 1
                    if int(nodelist[1]) > 500 and int(nodelist[1]) <= 1000:
                        self.t_totle[sampler]['lt_1000'] += 1
                    if int(nodelist[1]) > 1000:
                        self.t_totle[sampler]['gt_1000'] += 1
                    self.t_totle[sampler]['sample'].append(int(nodelist[1]))
                    self.t_totle[sampler]['timestamp'].append(int(nodelist[0]))
                    self.t_totle[sampler]['totle_time'] += int(nodelist[1])
                    self.t_totle[sampler]['succ_num'] += 1
                    if nodelist[7] == 'false':
                        self.t_totle[sampler]['assert_fails'] += 1
                else:
                    self.t_totle[sampler]['fail_num'] += 1
        self.calculate()
    

    def calculate(self):
        """calculate performance data from sample
        """
        self.aggregate = {}
        for sampler, rlt in self.t_totle.items():
            self.aggregate[sampler] = {}
            t_sorted = sorted(rlt['sample']) 
            endtime = sorted(rlt['timestamp'])[-1] if rlt['timestamp'] else 0
            starttime = sorted(rlt['timestamp'])[0] if rlt['timestamp'] else 0
            totle = len(t_sorted)
            line_90 = t_sorted[:int(totle*0.9)][-1] if totle else 0
            median = (t_sorted[int(round(totle/2))] + t_sorted[int(round(totle/2))+1])/2 if t_sorted else 0
            average_time = rlt['totle_time']/totle if rlt['totle_time'] else 0
            #self.aggregate[sampler]["totle_query"] = str(totle)
            self.aggregate[sampler]["average_time"] = str(average_time)
            self.aggregate[sampler]["succ_num"] = str(rlt['succ_num'])
            self.aggregate[sampler]["max_response_time"] = str(t_sorted[-1]) if t_sorted else 0
            self.aggregate[sampler]["min_response_time"] = str(t_sorted[0]) if t_sorted else 0
            self.aggregate[sampler]["QPS"] =(float(totle)/(endtime-starttime))*1000 if endtime and starttime else 0
            self.aggregate[sampler]["90%_line"] = str(line_90)
            self.aggregate[sampler]["median"] = str(median)
            self.aggregate[sampler]['Assert_Fails_num'] = str(rlt['assert_fails'])
            self.aggregate[sampler]['fail_num'] = str(rlt['fail_num'])
            response_time_distrib = ''
            response_time_distrib += '<200ms: ' + str(float(rlt['lt_200'])/totle if totle else 0)
            response_time_distrib += '; 200_to_500ms: '+ str(float(rlt['lt_500'])/totle if totle else 0)
            response_time_distrib += '; 500_to_1000ms: ' + str(float(rlt['lt_1000'])/totle if totle else 0)
            response_time_distrib += '; >1000ms: ' + str(float(rlt['gt_1000'])/totle if totle else 0)
            self.aggregate[sampler]['response_time_distribute'] = response_time_distrib

        self.format_print(self.aggregate)
            
        
        
    def format_print(self,aggregate):
    
        spaceing = 30
        for k,v in aggregate.items():
            print "\033[1;31;40m%s\033[0m" %k
            for name,value in v.items():
                print name.ljust(spaceing),value

if __name__=="__main__":
    anaJ = analyse_jmeter(r"/home/perf/performance/ontology_ask/log/rlt.jtl")
    if sys.argv[1] == 'xml':
        node = anaJ.read_xml()
        aggr = anaJ.get_aggregate_report(node)
    else:
        node = anaJ.read_file('plain')
        aggr = anaJ.get_plain_aggregate_report(node)
    

    


