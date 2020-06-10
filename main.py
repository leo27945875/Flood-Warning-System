from receiver import Receiver
from floodModel import Model
import twd97_to_wgs84
import args
import time
import json
import random
import datetime
import threading


def IoTInit():

    global receiver, model

    args.Init()
    args.receiver = Receiver(args.serverURL, args.regAddr)
    args.model = Model(source=args.coordinateImage,
                       target=args.floodRange,
                       mask=0.,
                       start=args.start,
                       startOnGrid=args.startOnGrid,
                       export=True)()

    receiver = args.receiver
    model = args.model


def SaveHeightData(file, height):
    now = datetime.datetime.now()
    date = f"{now.year}/{now.month}/{now.day}"
    clock = f"{now.hour}:{now.minute}:{now.second}"
    data = f"{date}, {clock}, {height}"
    print(data+"(cm)")
    file.write(data+"\n")
    file.flush()


def ReceiveFloodHeight():

    global receiver

    receiver.ReceiveData(updateTime=args.updateTime)


def MakeFloodRangeImage():

    global model

    oldHeight = -1e100
    with open(args.heightData, "a") as f:
        while True:
            if args.mode == "real":
                height = receiver.height
            elif args.mode == "test":
                height = random.randint(0, 10)
            else:
                raise ValueError("args.mode must be one of 'real' or 'test'")

            SaveHeightData(file=f, height=height)

            if height and abs(height-oldHeight) >= 0.3:
                height = 0. if height <= 0. else height
                oldHeight = height
                print("------------Making Flood Range Image-----------")
                model.Tune(height, export=True)
                print("-"*50+'\n')

            time.sleep(args.updateTime)


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
    coordinate = twd97_to_wgs84.GetLatLng()
    with open(args.root+"coordinate.json", "w") as f:
        json.dump(coordinate, f)

    print("Got the coordinate of monited range !")
