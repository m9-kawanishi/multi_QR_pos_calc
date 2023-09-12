import cv2
from pyzbar.pyzbar import decode

# rMQRコードを読み取る関数
def read_rmqr_code(image_path):
    try:
        # 画像を開いてrMQRコードを読み取る
        image = cv2.imread(image_path)
        decoded_objects = decode(image)

        for obj in decoded_objects:
            if obj.type == 'RMQR':
                return obj.data.decode('utf-8')

        return None
    except Exception as e:
        print(f"Error reading rMQR code: {e}")
        return None

# 画像ファイルのパス
image_path = 'rMQR_salmon riceball 1_balanced.png'  # 画像のパスを指定してください
img = cv2.imread(image_path)
if not img:
    print("SS")

# rMQRコードを読み取る
result = read_rmqr_code(image_path)

if result:
    print(f"rMQRコードデータ: {result}")
else:
    print("rMQRコードが見つかりませんでした。")
