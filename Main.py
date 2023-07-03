# -*- coding: utf-8 -*-

import Bot as bt
import DepthCam as dc
import WhelCon as wc
import threading

#人を認識した際の距離による処理
def parson_check (nm, dis):
    f1 = open('objudge.txt', 'w')
    f2 = open('disjudge.txt', 'w')
    if nm == "person":
        print ("人間を確認しました")
        f1.write(1)
        f2.write(1)
        print ("ゴミ箱と人間の距離は" + str(dis) + "cmです。")
        if (dis <= 0.75) and (dis != 0.0):
            f2.write(0)
            print("距離が近くなってきたので停止します")
    else:
        print("人を認識できていません")
        f1.write('0')
        f2.write('0')
    f1.close()
    f2.close()

def whel_jtalk():
    f1 = open('wheljudge.txt', 'r')
    a = f1.read()
    if a == '1':
        bt.jtalk('ついていきます')
    elif a == '2':
        bt.jtalk('とまりました')
    elif a == '3':
        bt.jtalk('見つけました')
    elif a == '4':
        bt.jtalk('見つかりませんでしたので停止します')
    elif a == '5':
        bt.jtalk('どこですか')


def main():
    x = 0
    bth = threading.Thread(target=bt.voice_recognition)
    dth = threading.Thread(target=dc.image_recognition)
    wth = threading.Thread(target=wc.wheel_control)
    bth.setDaemon(True)
    dth.setDaemon(True)
    wth.setDaemon(True)
    bth.start()
    dth.start()
    f1 = open('btjudge.txt', 'r')
    f2 = open('distance.txt', 'r')
    f3 = open('obj.txt', 'r')
    f4 = open('start.txt', 'w')
    while True:
        whel_jtalk()
        btj = f1.read()
        dis = f2.read()
        dis = dis.replace('\'', ' ')
        float(dis)
        obj = f3.read()
        if btj == 2:
            print('メインプログラムを終了します')
            break
        elif btj == '1':
            pasrson_check(obj, dis)
            if x == 0:
                x = 1
                wth.start()
            elif x == 1:
                f4.write('1')
        elif btj == '0':
            f4.write('0')
                
                

if __name__ == '__main__':

    main()
