from pypacian.pypacian import *
import pytest
import threading


def test_connect_handler():
    print(1)
    svconn = TcpHandler(host="127.0.0.1", src_port=50000, mode=MODE_SERVER)
    svconn.start()
    print(2)
    clconn = TcpHandler(ip="127.0.0.1", dst_port=50000, mode=MODE_CLIENT)
    clconn.start()
    print(3)
    clconn.stop()
    svconn.stop()

    # svconn = threading.Thread(target=server_connect, args=(["127.0.0.1", 50000]))
    # print(2)
    # clconn = threading.Thread(target=client_connect, args=(["127.0.0.1", 50000]))
    # print(3)
    # svconn.start()
    # print(4)
    # clconn.start()
    # svconn.join()
    # clconn.join()
