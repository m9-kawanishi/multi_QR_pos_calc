from pyzbar.pyzbar import decode
from PIL import Image
from pandas import DataFrame
import numpy as np
import cv2

from orientation_QR import get_qr_coords

# 4K キャリブレーション ELPカメラ（川西）
cmtx = np.array([[2.24861379e+03, 0.00000000e+00, 2.01502882e+03],
                        [0.00000000e+00, 2.25437686e+03, 1.28473568e+03],
                        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
dist = np.array([[ 8.71390681e-02, -1.93136080e-01,  4.63674412e-04,  1.50404867e-04, 1.79991456e-01]])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # QRコードを検出
    decoded_objects = decode(frame)
    
    # 検出したQRコードを描画
    for obj in decoded_objects:
        points = obj.polygon
        
        if len(points) > 4:
            # 矩形を描画
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            cv2.polylines(frame, [hull], True, (0, 255, 0), 2)

            # 位置姿勢を推定および描画
            axis_points, rvec, tvec = get_qr_coords(cmtx, dist, points)
            print(axis_points)

            #BGR color format
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)]

            #check axes points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4,2))

                a = int((axis_points[0][0]+axis_points[1][0]+axis_points[2][0]+axis_points[3][0])/4)
                b = int((axis_points[0][1]+axis_points[1][1]+axis_points[2][1]+axis_points[3][1])/4)

                origin = (int(axis_points[0][0]),int(axis_points[0][1]))

                for p, c in zip(axis_points[1:], colors[:3]):
                    p = (int(p[0]), int(p[1]))

                    #Sometimes qr detector will make a mistake and projected point will overflow integer value. We skip these cases. 
                    if origin[0] > 5*frame.shape[1] or origin[1] > 5*frame.shape[1]:break
                    if p[0] > 5*frame.shape[1] or p[1] > 5*frame.shape[1]:break

                    cv2.line(frame, origin, p, c, 5)

        
        else:
            # -- 矩形を描画 --
            for j in range(4):
                cv2.line(frame, points[j], points[(j+1) % 4], (0, 255, 0), 3)

            # -- 位置姿勢を推定および描画 --
            # ---- ndarrayに変換 ----
            points = np.array([[[point.x, point.y] for point in points]])
            points = points.astype(float)
            axis_points, rvec, tvec = get_qr_coords(cmtx, dist, points)

            #BGR color format
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)]

            #check axes points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4,2))

                a = int((axis_points[0][0]+axis_points[1][0]+axis_points[2][0]+axis_points[3][0])/4)
                b = int((axis_points[0][1]+axis_points[1][1]+axis_points[2][1]+axis_points[3][1])/4)

                origin = (int(axis_points[0][0]),int(axis_points[0][1]))

                for p, c in zip(axis_points[1:], colors[:3]):
                    p = (int(p[0]), int(p[1]))

                    #Sometimes qr detector will make a mistake and projected point will overflow integer value. We skip these cases. 
                    if origin[0] > 5*frame.shape[1] or origin[1] > 5*frame.shape[1]:break
                    if p[0] > 5*frame.shape[1] or p[1] > 5*frame.shape[1]:break

                    cv2.line(frame, origin, p, c, 5)
    
        # QRコードのデータを表示
        cv2.putText(frame, str(obj.data), (obj.rect.left, obj.rect.top), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    
    # ウィンドウにフレームを表示
    cv2.imshow("QR Code Detection", frame)
    
    # 'q' キーを押してループを中断
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースの解放
cap.release()
cv2.destroyAllWindows()




