#!/usr/bin/env python
# coding: utf-8
#

''' import modules
'''
from scapy.all import *


class TCP_CONNECT:

    def __init__(self,
                 src = '127.0.0.1',
                 dst = '127.0.0.1',
                 sport = 60000,
                 dport = 60000):
        self.src = src
        self.dst = dst
        self.sport = sport
        self.dport = dport
        self.ip = IP(dst = self.dst)
        self.tcp = TCP(sport = self.sport, dport = self.dport, flags = 'S', seq = 100)

    def synchronize(self):
        ''' request for TCP connection
        '''
        # send sync & get ack
        syn = self.ip / self.tcp
        self.syn_ack = sr1(syn)
        # send sync
        self.tcp.seq += 1
        self.tcp.ack = self.syn_ack.seq + 1
        self.tcp.flags = 'A'
        ack = self.ip / self.tcp
        send(ack)
        return syn, self.syn_ack, ack

    
    def fin(self):
        ''' finish for TCP connection
        '''

        # send FIN packet
        self.tcp.seq 
        fin = self.ip / TCP(sport = self.sport,
                            dport = self.dport,
                            flags = 'FA',
                            seq = self.syn_ack.ack,
                            ack = self.syn_ack.seq + 1)
        self.fin_ack = sr1(fin)

        # return final ACK
        lastack = self.ip / TCP(sport = self.sport,
                                dport = self.dport,
                                flags = 'A',
                                seq = self.fin_ack.ack,
                                ack = self.fin_ack.seq + 1)
        # self.tcp.ack = fin_ack.seq + 1
        # self.tcp
        # self.tcp.flags = 'A'
        # send(self.ip / self.tcp)
        send(lastack)
        
    def __del__(self):
        self.fin()
    
