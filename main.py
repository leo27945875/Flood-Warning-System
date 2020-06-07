from receiver import Receiver
from floodModel import Model
import twd97_to_wgs84
import args
import time
import json
import threading

# IoT setting:
args.Init()
args.receiver = Receiver(args.serverURL, args.regAddr)
args.model = Model(args.geometryImage, args.floodRange,
                   0., args.start, args.startOnGrid, export=True)()
receiver = args.receiver
model = args.model


def ReceiveFloodHeight():

    global receiver

    receiver.ReceiveData()


def MakeFloodRangeImage():

    global model

    oldHeight = -1.
    while True:
        height = receiver.height
        if height and height > 0. and (height != oldHeight):
            oldHeight = height
            print("------------Making Flood Range Image-----------")
            model.Tune(height, export=True)
            print("-"*50+'\n')

        time.sleep(1)


def Main():
    # Multi-thread:
    thread0 = threading.Thread(
        target=ReceiveFloodHeight, name="ReceiveFloodHeight")
    thread1 = threading.Thread(
        target=MakeFloodRangeImage, name="MakeFloodRangeImage")
    thread0.start()
    thread1.start()

    # Export geometry data:
    geo = twd97_to_wgs84.GetLatLng()
    with open("./data/geometry.json", "w") as f:
        json.dump(geo, f)


if __name__ == "__main__":
    Main()
