from pypacian.pypacian import *
import pytest
import threading


def test_connect_handler():
    svconn = TcpHandler(host="127.0.0.1", src_port=50000, mode=MODE_SERVER)
    svconn.start()
    clconn = TcpHandler(ip="127.0.0.1", dst_port=50000, mode=MODE_CLIENT)
    clconn.start()
    clconn.stop()
    svconn.stop()
