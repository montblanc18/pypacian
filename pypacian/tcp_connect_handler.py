#!/usr/bin/env python
# coding: utf-8
#

''' import modules
'''
from scapy.all import *

__NOT_ESTABLISHED__ = 'NOT Established'
__ESTABLISHED__ = 'Established'


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
        self.status = __NOT_ESTABLISHED__

        
    def synchronize(self):
        ''' request for TCP connection
        '''
        self.tcp.flags = 'S'
        # send sync & get ack
        syn = self.ip / self.tcp
        self.syn_ack = sr1(syn)
        # send sync
        self.tcp.seq += 1
        self.tcp.ack = self.syn_ack.seq + 1
        self.tcp.flags = 'A'
        ack = self.ip / self.tcp
        send(ack)
        self.status = __ESTABLISHED__
        return syn, self.syn_ack, ack

    def wait_for_syn(self):
        ''' wait for syn packet from a client as a server
        '''
        filter_rule = 'tcp and port %d' % self.sport
        while True:
            ''' listen 1 packet & analyze it 
            '''
            pkt = sniff(filter = filter_rule, count = 1)
            try:
                if pkt[TCP].flags == 'S':
                    break
            except IndexError:
                pass
        syn_ack = self.ip / TCP(sport = self.sport,
                                dport = self.dport,
                                flags = 'SA',
                                seq = pkt.ack,
                                ack = pkt.seq + 1)
        pkt = sr1(syn_ack)
        if pkt[TCP].flags == 'A':
            self.status = __ESTABLISHED__
            return
        else:
            self.reset()
            return
        
    def reset(self):
        ''' to be written
        '''
        pass
            


    
    def finish(self):
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
        self.finish()
    
