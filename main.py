from receiver import Receiver
from flood_model import Model
import twd97_to_wgs84
import args
import time
import json
import random
import pytz
import datetime
import threading


def IoTInit():
    """
    Initialize the environment of this IoT project setting:
    """

    global receiver, model, timezone, ReceiveData

    print("Initializing the setting of IoT ...")
    args.Init()
    args.receiver = Receiver(args.serverURL, args.regAddr)
    args.model = Model(source=args.coordinateImage,
                       target=args.floodRange,
                       mask=0.,
                       start=args.start,
                       startOnGrid=args.startOnGrid,
                       export=True)()

    def ReceiveDataFunc():
        if args.mode == "real":
            height = receiver.height
        elif args.mode == "test":
            height = random.randint(0, 10)
        else:
            raise ValueError("args.mode must be one of 'real' or 'test'")

        return height

    receiver = args.receiver
    model = args.model
    timezone = pytz.timezone(args.timezone)
    ReceiveData = ReceiveDataFunc


def SaveHeightData(file, height):
    """
    Save the flood height data received from the IoT device to a CSV file:
    """

    now = datetime.datetime.now(timezone)
    date = f"{now.year}/{now.month}/{now.day}"
    clock = f"{now.hour}:{now.minute}:{now.second}"
    data = f"{date}, {clock}, {height}"
    print(data+"(cm)")
    file.write(data+"\n")
    file.flush()


def ReceiveFloodHeight():
    """
    Receive the flood height data detected by the IoT device:
    """

    print("Start receiving height data !")
    receiver.ReceiveData(updateTime=args.updateTime)


def MakeFloodRangeImage():
    """
    Make images of the range of the flood:
    """

    time.sleep(3)
    print("Start making flood range image !\n"+"="*50+"\n")
    with open(args.heightData, "a") as f:
        oldHeight = -1e100
        while True:
            height = ReceiveData()
            if height:
                SaveHeightData(file=f, height=height)
                height = 0. if height <= 0. else height
                if abs(height-oldHeight) >= 0.3:
                    print("-------------Making Flood Range Image-------------")
                    model.Tune(height, export=True)
                    print("-"*50+'\n')
                    oldHeight = height

            time.sleep(args.updateTime)


def Main():
    """
    The main program of this IoT project:
    """

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
