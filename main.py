from receiver import Receiver
from floodModel import Model
import twd97_to_wgs84
import args
import time
import json
import threading


def IoTInit():

    global receiver, model

    args.Init()
    args.receiver = Receiver(args.serverURL, args.regAddr)
    args.model = Model(args.coordinateImage, args.floodRange,
                       0., args.start, args.startOnGrid, export=True)()
    receiver = args.receiver
    model = args.model


def ReceiveFloodHeight():

    global receiver

    receiver.ReceiveData(file=args.root+"flood_height.csv",
                         updateTime=args.updateTime)


def MakeFloodRangeImage():

    global model

    oldHeight = -1.
    while True:
        height = receiver.height
        if height and (height != oldHeight):
            height = 0. if height < 0. else height
            oldHeight = height
            print("------------Making Flood Range Image-----------")
            model.Tune(height, export=True)
            print("-"*50+'\n')

        time.sleep(args.updateTime*0.5)


def Main():
    # IoT setting:
    IoTInit()

    # Multi-thread:
    thread0 = threading.Thread(
        target=ReceiveFloodHeight, name="ReceiveFloodHeight")
    thread1 = threading.Thread(
        target=MakeFloodRangeImage, name="MakeFloodRangeImage")
    thread0.start()
    thread1.start()

    # Export coordinate data:
    print("Get the coordinate of monited range !")
    coordinate = twd97_to_wgs84.GetLatLng()
    with open(args.root+"coordinate.json", "w") as f:
        json.dump(coordinate, f)


if __name__ == "__main__":
    Main()
