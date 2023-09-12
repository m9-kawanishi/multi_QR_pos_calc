from rmqrcode import rMQR
import rmqrcode
from rmqrcode import QRImage
import sys

# pip install rmqrcode
# v0.3.1
# https://github.com/OUDON/rmqrcode-python#readme

# generate
data = "https://www.sciencedirect.com/science/article/pii/S0031320314000235"

while True:
    print("1 : balanced \n2 : minimize_width \n3 : minimize_height")
    input_num = int(input("please input number 1~3 >> "))
    if input_num in (1, 2, 3):
        break

if input_num == 1:
    option = "balanced"
    qr = rMQR.fit(
        data,
        ecc=rmqrcode.ErrorCorrectionLevel.M,
        fit_strategy=rmqrcode.FitStrategy.BALANCED
    )
    
elif input_num == 2:
    option = "mini_width"
    qr = rMQR.fit(
        data,
        ecc=rmqrcode.ErrorCorrectionLevel.M,
        fit_strategy=rmqrcode.FitStrategy.MINIMIZE_WIDTH
    )

elif input_num == 3:
    option = "mini_height"
    qr = rMQR.fit(
        data,
        ecc=rmqrcode.ErrorCorrectionLevel.M,
        fit_strategy=rmqrcode.FitStrategy.MINIMIZE_HEIGHT
    )

# ecc : ErrorCorrectionLevel
    # ErrorCorrectionLevel.M: Approx. 15% Recovery Capacity.
    # ErrorCorrectionLevel.H: Approx. 30% Recovery Capacity.

# fit_strategy : specify how to determine size of rMQR Code.
    # FitStrategy.MINIMIZE_WIDTH: Try to minimize width.
    # FitStrategy.MINIMIZE_HEIGHT: Try to minimize height.
    # FitStrategy.BALANCED: Try to keep balance of width and height.

# Save as Image
image = QRImage(qr, module_size = 128)
# image.show()
# image.save(f"rMQR_{data}_{option}.png")
image.save(f"rMQR_{option}.png")