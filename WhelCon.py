# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO

#GPIOセットアップ
#GPIOピンの基盤の番号で指定する
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(基盤のピン番号, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
#GPIO.output(基盤のピン番号, GPIO.LOW)
#GPIO.output(基盤のピン番号, GPIO.HIGH)
#右ホイール
GPIO.output(5, GPIO.LOW)
GPIO.output(7, GPIO.HIGH)
#左ホイール
GPIO.output(13, GPIO.LOW)
GPIO.output(11, GPIO.HIGH)
#中央ホイール
GPIO.output(10, GPIO.LOW)
GPIO.output(12, GPIO.HIGH)
#PWMセットアップ
#変数 = GPIO.PWM(基盤のピン番号, デューティー比)
r = GPIO.PWM(3, 50)
l = GPIO.PWM(15, 50)
c = GPIO.PWM(8, 50)
#スタンバイOK
#変数.start(出力値)
r.start(0)
l.start(0)
c.start(0)

#直進処理
def straight():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(5, GPIO.HIGH)
    GPIO.output(7, GPIO.LOW)
    r.ChangeDutyCycle(80)
    l.ChangeDutyCycle(80)
    c.ChangeDutyCycle(0)

#旋回処理
def turn():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.HIGH)
    r.ChangeDutyCycle(80)
    l.ChangeDutyCycle(80)
    c.ChangeDutyCycle(80)

#一時停止処理
def stop():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    r.ChangeDutyCycle(0)
    l.ChangeDutyCycle(0)
    c.ChangeDutyCycle(0)

#会話終了時処理
def end():
    GPIO.output(13, GPIO.LOW)
    GPIO.output(11, GPIO.LOW)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(10, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    r.ChangeDutyCycle(0)
    l.ChangeDutyCycle(0)
    c.ChangeDutyCycle(0)
    GPIO.cleanup()


def wheel_control():
    t_end = time.time() + 1 * 15
    f1 = open('objudge.txt', 'r')
    f2 = open('disjudge.txt', 'r')
    f3 = open('wheljudge.txt', 'w')
    f4 = open('start.txt', 'r')
    try:
        while True:
            obj = f1.read()
            dij = f2.read()
            if obj == '1':
                if dij == '0':
                    stop()
                    print('とまりました')
                    f3.write('2')
                    while True:
                        st = f4.read()
                        if st == '1':
                            break
                else:
                    straight()
                    print('ついていきます')
                    f3.write('1')
            else:
                turn()
                while time.time() < t_end:
                    print('どこですか')
                    f3.write('5')
                    obj = f1.read()
                    if obj == '1':
                        print('見つけました')
                        f3.write('3')
                        break
                print('みつかるませんでしたので停止します')
                f3.write('4')
                stop()

    finally:
        end()
        f1.close()
        f2.close()
        f3.close()

if __name__ == '__main__':
    wheel_control()
