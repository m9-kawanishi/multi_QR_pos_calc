import cv2 as cv
import numpy as np
import sys


def show_axes(cmtx, dist, in_source):

    cap = cv.VideoCapture(in_source)

    qr = cv.QRCodeDetector()

    while True:
        ret, img = cap.read()
        if ret == False: break

        # ret_qr, points = qr.detect(img)
        ret_qr, decoded_info, points, straight_qrcode = qr.detectAndDecodeMulti(img)
        if points is None:
            pass
        else:
            print(f"points : {points}")
            print(f"points : {type(points)}")

        if ret_qr:
            axis_points, rvec, tvec = get_qr_coords(cmtx, dist, points)

            #BGR color format
            colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0,0,0)]

            #check axes points are projected to camera view.
            if len(axis_points) > 0:
                axis_points = axis_points.reshape((4,2))

                a = int((axis_points[0][0]+axis_points[1][0]+axis_points[2][0]+axis_points[3][0])/4)
                b = int((axis_points[0][1]+axis_points[1][1]+axis_points[2][1]+axis_points[3][1])/4)

                origin = (int(axis_points[0][0]),int(axis_points[0][1]))
                # origin = (a, b)

                for p, c in zip(axis_points[1:], colors[:3]):
                    p = (int(p[0]), int(p[1]))

                    #Sometimes qr detector will make a mistake and projected point will overflow integer value. We skip these cases. 
                    if origin[0] > 5*img.shape[1] or origin[1] > 5*img.shape[1]:break
                    if p[0] > 5*img.shape[1] or p[1] > 5*img.shape[1]:break

                    cv.line(img, origin, p, c, 5)

        cv.imshow('frame', img)

        k = cv.waitKey(20)
        if k == 27: break #27 is ESC key.

    cap.release()
    cv.destroyAllWindows()

def get_qr_coords(cmtx, dist, points):

    #Selected coordinate points for each corner of QR code.
    qr_edges = np.array([[0,0,0],
                         [0,1,0],
                         [1,1,0],
                         [1,0,0]], dtype = 'float32').reshape((4,1,3))

    #determine the orientation of QR code coordinate system with respect to camera coorindate system.
    ret, rvec, tvec = cv.solvePnP(qr_edges, points, cmtx, dist)

    #Define unit xyz axes. These are then projected to camera view using the rotation matrix and translation vector.
    unitv_points = np.array([[0,0,0], [1,0,0], [0,1,0], [0,0,1]], dtype = 'float32').reshape((4,1,3))
    if ret:
        points, jac = cv.projectPoints(unitv_points, rvec, tvec, cmtx, dist)
        #the returned points are pixel coordinates of each unit vector.
        return points, rvec, tvec

    #return empty arrays if rotation and translation values not found
    else: return [], [], []

    

if __name__ == '__main__':

    # 4K キャリブレーション ELPカメラ（川西）
    cmtx = np.array([[2.24861379e+03, 0.00000000e+00, 2.01502882e+03],
                            [0.00000000e+00, 2.25437686e+03, 1.28473568e+03],
                            [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
    dist = np.array([[ 8.71390681e-02, -1.93136080e-01,  4.63674412e-04,  1.50404867e-04, 1.79991456e-01]])

    show_axes(cmtx, dist, 0)
    