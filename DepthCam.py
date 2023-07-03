# -*- coding: utf-8 -*-

import pyrealsense2 as rs
import numpy as np
import cv2
import torch

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

#YOLOのモデルをロード
model = torch.hub.load('ultralytics/yolov5', 'yolov5s') 


#YOLOを使った物体検出
def output_distance(predict_result, depth_frame):
    name = ""
    distance = 0
    #推論結果を取得
    obj = predict_result.pandas().xyxy[0]

    #バウンディングボックスの情報を取得
    for  i in range(len(obj)):
        name = obj.name[i]
        xmin = obj.xmin[i]
        ymin = obj.ymin[i]
        xmax = obj.xmax[i]
        ymax = obj.ymax[i]

        #中央座標計算
        x_length = xmax - xmin #バウンディングボックス長さ
        y_length = ymax - ymin #バウンティングボックス高さ

        x_center = xmin + (x_length / 2) #中央X座標
        y_center = ymin + (y_length / 2) #中央y座標

        #距離を取得
        distance = depth_frame.get_distance(int(x_center), int(y_center))
        print(name + "," + str(distance))
        return (name, distance)
    return ("None", 0)

#メイン処理
def image_recognition():
    #ストリーミングの開始
    pipeline.start(config)

    try:
        while True:

            #フレームのコヒーレントペアを待つ(深度と色)
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            #取得した画像をnumpy配列に変換
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            #推論実行
            #color_image = predict(color_image)
            result = model(color_image)
            result.render()
            color_image = result.ims[0]

            #距離を出力
            (nam, dist) = output_distance(result, depth_frame)
            
            f1 = open('obj.txt', 'w')
            f2 = open('distance.txt', 'w')
            f1.write(nam)
            f2.write(str(dist))

            
            '''
            #深度画像にカラーマップを適用 (最初に画像を 8 ビット/ピクセルに変換する必要がある)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            #二つの画像を水平方向に重ねる
            images = np.hstack((color_image, depth_colormap))
            #表示
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            cv2.waitKey(1)
            '''

    finally:

        #ストリーミング停止
        pipeline.stop()


