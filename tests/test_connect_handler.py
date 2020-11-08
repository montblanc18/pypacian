import pypacian.pypacian


def test_connect_handler():
    pypacian.server_connect("127.0.0.1", 50000)
    pypacian.client_connect("127.0.0.1", 50000)
