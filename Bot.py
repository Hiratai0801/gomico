# -*- coding: utf-8 -*-
import socket
import time
import subprocess
import random


def jtalk(tt):
    open_jtalk=['open_jtalk']
    mech=['-x','/var/lib/mecab/dic/open-jtalk/naist-jdic']
    htsvoice=['-m','/usr/share/hts-voice/mei/mei_normal.htsvoice']
    speed=['-r','1.0']
    outwav=['-ow','open_jtalk.wav']
    cmd=open_jtalk+mech+htsvoice+speed+outwav
    subprocess.run(cmd,input=tt.encode())
    aplay = ['aplay','-q','open_jtalk.wav']
    subprocess.run(aplay)


def voice_recognition():

    #julius接続の際に使用する変数
    host = 'localhost'
    port = 10500
    # Juliusに接続する準備
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    #初期値
    i = 2 #判定で使う値の初期値
    res = '' #文字列の初期値
    #判定ファイルオープン
    f1 = open('btjudge.txt', 'w')
    f1.write('0')

    while True:
        # 音声認識の区切りである「改行+.」がくるまで待つ
        while (res.find('\n.') == -1):
            # Juliusから取得した値を格納していく
            res += sock.recv(1024).decode()

        word = ''
        for line in res.split('\n'):

            # Juliusから取得した値から認識文字列の行を探す
            index = line.find('WORD=')
            # 認識文字列があったら...
            if index != -1:
                # 認識文字列部分だけを抜き取る
                line = line[index + 6 : line.find('"', index + 6)]
                # 文字列の開始記号以外を格納していく
                if line != '[s]':
                    word = word + line
                    print(word)

            res = ''
            if word == 'おっけいゴミこ':
                print('返答：ごようはなんでしょうか')
                jtalk(u'ごようはなんでしょうか')
                time.sleep(4)
                f1.write('0')

                while True:

                    while (res.find('\n.') == -1):
                        # Juliusから取得した値を格納していく
                        res += sock.recv(1024).decode()

                    word = ''
                    for line in res.split('\n'):
                        if i == 1:
                            break

                        # Juliusから取得した値から認識文字列の行を探す
                        index = line.find('WORD=')
                        # 認識文字列があったら...
                        if index != -1:
                            # 認識文字列部分だけを抜き取る
                            line = line[index + 6 : line.find('"', index + 6)]
                            # 文字列の開始記号以外を格納していく
                            if line != '[s]':
                                word = word + line
                                print(word)
                            # 文字列を認識したら...
                        if word == 'おはよう':
                            jtalk(u'おはようございます')
                            print('返答：おはようございます')
                            time.sleep(4)
                            f1.write('0')
                        if word == 'こんにちは':
                            jtalk(u'こんにちは')
                            print('返答：こんにちは' )
                            time.sleep(4)
                            f1.write('0')
                        if word == 'こんばんは':
                            jtalk(u'こんばんは')
                            print('返答：こんばんは' )
                            time.sleep(4)
                            f1.write('0')
                        elif word == 'じこしょうかいをして':
                            jtalk(u'はい、わかりました。　私はの名前はごみ箱　あなたの生活をサポートします。')
                            print('返答：はい、わかりました。　私はの名前はごみ箱　あなたの生活をサポートします。' )
                            time.sleep(4)
                            f1.write('0')
                        elif word == 'うたって':
                            time.sleep(1)
                            f1.write('0')
                            print(0)
                        elif word == 'ついてきて':
                            jtalk(u'はい、ついていきます')
                            time.sleep(4)
                            f1.write('1')

                        res = ''

                        if word == 'ばいばいゴミこ':
                            i = 1
                            break
                    if i == 1:
                        break
                if i == 1:
                    break
            if i == 1:
                break
        if i == 1:
            jtalk(u'ばいばい')
            f1.write('2')
            f1.close()

            break

if __name__ == '__main__':

    voice_recognition()
