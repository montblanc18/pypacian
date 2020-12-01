#!/usr/bin/env python
# coding: utf-8
#

""" import modules
"""
from scapy.all import *
import copy
import socket
import threading

__NOT_ESTABLISHED__ = "NOT Established"
__ESTABLISHED__ = "Established"
MODE_CLIENT = "CLIENT"
MODE_SERVER = "SERVER"


class TCP_CONNECT:
    def __init__(self, src="127.0.0.1", dst="127.0.0.1", sport=60000, dport=60000):
        self.src = src
        self.dst = dst
        self.sport = sport
        self.dport = dport
        self.ip = IP(dst=self.dst)
        self.tcp = TCP(sport=self.sport, dport=self.dport, flags="S", seq=100)
        self.rcv_pkt = self.ip / self.tcp
        self.status = __NOT_ESTABLISHED__

    def synchronize(self):
        """request for TCP connection"""
        self.tcp.flags = "S"
        """ send sync & get ack
        """
        syn = self.ip / self.tcp
        # self.syn_ack = sr1(syn)
        self.rcv_pkt = sr1(syn)
        """ send sync
        """
        self.tcp.seq += 1
        # self.tcp.ack = self.syn_ack.seq + 1
        self.tcp.ack = self.rcv_pkt.seq + 1
        self.tcp.flags = "A"
        ack = self.ip / self.tcp
        send(ack)
        self.status = __ESTABLISHED__
        return syn, self.syn_ack, ack

    def wait_for_syn(self):
        """wait for syn packet from a client as a server"""
        filter_rule = "tcp and port %d" % self.sport
        while True:
            """listen 1 packet & analyze it"""
            pkt = sniff(filter=filter_rule, count=1)
            try:
                if pkt[TCP].flags == "S":
                    break
            except IndexError:
                pass
        self.rcv_pkt = pkt
        syn_ack = self.ip / TCP(
            sport=self.sport,
            dport=self.dport,
            flags="SA",
            seq=self.rcv_pkt.ack,
            ack=self.rcv_pkt.seq + 1,
        )
        # seq = pkt.ack,
        # ack = pkt.seq + 1)
        self.rcv_pkt = sr1(syn_ack)
        try:
            if self.rcv_pkt[TCP].flags == "A":
                self.status = __ESTABLISHED__
                return
            else:
                self.reset()
        except IndexError:
            self.reset()
        return

    def send_camouflage_tcp(self, load):
        self.tcp.flags = "PA"
        self.tcp.seq = self.rcv_pkt.ack
        self.tcp.seq = self.rcv_pkt.seq + len(self.rcv_pkt.load)
        pkt = self.ip / self.tcp / load
        self.rcv_pkt = sr1(pkt)

    def reset(self):
        """send RST packet
        to be confirmed...
        """
        self.tcp.flags = "R"
        reset_pkt = self.ip / self.tcp
        send(reset_pkt)

    def finish(self):
        """finish for TCP connection"""

        """ send FIN packet
        """
        fin = self.ip / TCP(
            sport=self.sport,
            dport=self.dport,
            flags="FA",
            seq=self.rcv_pkt.ack,
            ack=self.rcv_pkt.seq + 1,
        )
        # seq = self.syn_ack.ack,
        # ack = self.syn_ack.seq + 1)
        # self.fin_ack = sr1(fin)
        self.rcv_pkt = sr1(fin)

        # return final ACK
        lastack = self.ip / TCP(
            sport=self.sport,
            dport=self.dport,
            flags="A",
            seq=self.rcv_pkt.ack,
            ack=self.rcv_pkt.seq + 1,
        )
        # seq = self.fin_ack.ack,
        # ack = self.fin_ack.seq + 1)
        # self.tcp.ack = fin_ack.seq + 1
        # self.tcp
        # self.tcp.flags = 'A'
        # send(self.ip / self.tcp)
        send(lastack)

    def __del__(self):
        self.reset()
        # self.finish()


class TcpHandler(threading.Thread):
    def __init__(self, host="", ip="", src_port=0, dst_port=0, mode=""):
        super(TcpHandler, self).__init__()
        self.src_port = src_port
        self.dst_port = dst_port
        self.ip = ip
        self.host = host
        self.mode = mode
        print(mode)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        if self.mode == MODE_SERVER:
            print("setup server mode")
            self.sock.bind((self.host, self.src_port))
            self.sock.listen(1)
            while True:
                # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
                self.conn, self.addr = self.sock.accept()
            print("connected")
        elif self.mode == MODE_CLIENT:
            print("setup client mode")
            self.sock.connect((self.ip, self.dst_port))
        else:
            print("error")

    def stop(self):
        self.__del__()

    def __del__(self):
        self.sock.close()
