#!/usr/bin/env python
# coding: utf-8
#


""" import modules
"""
from scapy.all import *


""" import self-modules
"""
from pypacian.tcp_connect_handler import *
from pypacian.arp_spoofing import *
from pypacian.connect_handler import *


# キャプチャする機能
# + 定期的な時間周期 or ファイル量で保存するファイル形式を切り替える
# + ファイルの保存や切り替えのタイミングでパケットの抜けが生じないこと
# --> Wiresharkで十分では？？？
#

# pcapファイルを読み込んで吐き出す機能
# + 読み込んで、srcとdstを書き換える機能
# + 読み込んだ順にバースト的に吐き出す機能
# + 読み込んだ順に、送受信時刻を抑えて再送する機能
# ++ 時刻は「ファイルの開始時刻+timedelta」で差分を取ること。
# ++ timer割り込みを実行し、実行時間を過ぎているイベントがあれば実行すること。
# +++ なるべく軽量じゃないとここが分づまる
