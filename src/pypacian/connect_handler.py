#!/usr/bin/env python
# coding: utf-8
#

import socket


def server_connect(ip: str, port: int):
    # IPアドレスとポートを指定
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        # 1 接続
        s.listen(1)
        # connection するまで待つ
        while True:
            # 誰かがアクセスしてきたら、コネクションとアドレスを入れる
            conn, addr = s.accept()
            with conn:
                while True:
                    # データを受け取る
                    data = conn.recv(1024)
                    if not data:
                        break
                    print("data : {}, addr: {}".format(data, addr))
                    # クライアントにデータを返す(b -> byte でないといけない)
                    conn.sendall(b"Received: " + data)


def client_connect(ip: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # サーバを指定
        s.connect((ip, port))
        # サーバにメッセージを送る
        s.sendall(b"hello")
        # ネットワークのバッファサイズは1024。サーバからの文字列を取得する
        data = s.recv(1024)
        #
        print(repr(data))