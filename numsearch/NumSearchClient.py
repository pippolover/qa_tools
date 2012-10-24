#!/usr/bin/env python
# -*- coding=utf-8 -*-
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from numbersearch import NumberSearchService 
from numbersearch import ttypes

class NumSearchClient:
    def __init__(self, server='192.168.23.15', port=20000):
        ''' 
        Exceptions:
            raise ConnectionError exception when connection error
        '''
        transport = TSocket.TSocket(server, port)
        self.transport = TTransport.TBufferedTransport(transport)
        protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
        self.client = NumberSearchService.Client(protocol)
        self.transport.open()
    
    def __del__(self):
        self.transport.close()
    
    def getGid(self, uid, sen, time=1347360229098):
    
        print  self.client.doSentenceDe(uid, sen, time)


    def delUid(self, uid):
        self.client.deleteSentence(uid)

if __name__ == "__main__":
    nc = NumSearchClient()
    #nc.delUid("11111")
    #nc.delUid("22222")
    #nc.getGid("000000", "同比增长8成")
    nc.getGid("555555", "同比增长80%")
    #nc.getGid("444444", "同比增长8倍")
