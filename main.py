from receiver import Receiver
from flood_model import Model
from auto_email_sender import EmailSender
import twd97_to_wgs84
import args
import time
import json
import random
import pytz
import datetime
import threading
import smtplib
from email.mime.text import MIMEText


def IoTInit():
    """
    Initialize the environment of this IoT project setting:
    """

    global receiver, model, sender, timezone

    print("Initializing the setting of IoT ...")
    args.Init()
    args.receiver = Receiver(args.serverURL, args.regAddr)
    args.model = Model(source=args.coordinateImage,
                       target=args.floodRange,
                       mask=0.,
                       start=args.start,
                       startOnGrid=args.startOnGrid,
                       export=True)()
    args.sender = EmailSender(args.myGmail, args.myPW, args.addresses)

    receiver = args.receiver
    model = args.model
    sender = args.sender
    timezone = pytz.timezone(args.timezone)
    print("Finished initialization !")


def SaveHeightData(file, height):
    """
    Save the flood height data received from the IoT device to a CSV file:
    """

    now = datetime.datetime.now(timezone)
    date = f"{now.year}/{now.month}/{now.day}"
    clock = f"{now.hour}:{now.minute}:{now.second}"
    data = f"{date}, {clock}, {height}"
    print("\n"+data+"(cm)")
    file.write(data+"\n")
    file.flush()


def JudgeToSendEmail():
    """
    Judge whether need to send waring e-mail of the flood or not:
    """

    time.sleep(3)
    print("Start judging whether send e-mail or not !")
    sendTime = -1e100
    while True:
        currTime = time.time()
        if currTime - sendTime >= args.nextTimeInterval:
            height = receiver.height
            if height and height >= args.thresholds[0]:
                sender.SendFloodHeightMessages(f"絕望! 淹水已超過{height}公分!!")
                sendTime = currTime
            elif height and height >= args.thresholds[1]:
                sender.SendFloodHeightMessages(f"震驚! 淹水已超過{height}公分!!")
                sendTime = currTime
            elif height and height >= args.thresholds[2]:
                sender.SendFloodHeightMessages(f"注意! 淹水已超過{height}公分!!")
                sendTime = currTime

        time.sleep(10)


def ReceiveFloodHeight():
    """
    Receive the flood height data detected by the IoT device:
    """

    print("Start receiving height data !")
    receiver.ReceiveData(updateTime=args.updateTime, mode=args.mode)


def MakeFloodRangeImage():
    """
    Make images of the range of the flood:
    """

    time.sleep(4)
    print("Start making flood range image !\n"+"="*50+"\n")
    with open(args.heightData, "a") as f:
        oldHeight = -1e100
        while True:
            height = receiver.height
            if height is not None:
                SaveHeightData(file=f, height=height)
                height = 0. if height <= 0. else height
                if abs(height-oldHeight) >= 0.3:
                    print("-------------Making Flood Range Image-------------")
                    model.Tune(height, export=True)
                    print("-"*50+'\n')
                    oldHeight = height
            else:
                print("\nNo data received ...\n")

            time.sleep(args.updateTime-0.05)


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
    thread2 = threading.Thread(
        target=JudgeToSendEmail, name="JudgeToSendEmail")
    thread0.start()
    thread1.start()
    thread2.start()

    # Export coordinate data:
    coordinate = twd97_to_wgs84.GetLatLng()
    with open(args.root+"coordinate.json", "w") as f:
        json.dump(coordinate, f)

    print("Got the coordinate of monited range !")
