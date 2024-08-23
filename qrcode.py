from MyQR import myqr
import os
def createQr(data):
    myqr.run(
        words=data,
        picture='demo.jpg',
        colorized=True,
        version=1,
        save_name="demo.png"
    )