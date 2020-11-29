from pypacian.pypacian import *
import pytest


def test_connect_handler():
    server_connect("127.0.0.1", 50000)
    client_connect("127.0.0.1", 50000)
