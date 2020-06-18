from receiver import Receiver
from flood_model import Model
from auto_email_sender import EmailSender
from thingspeak_sender import ThingSpeakSender
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

    global receiver, model, emailSender, thingSpeakSender, timezone

    print("[Main] Initializing the setting of IoT ...")
    args.Init()
    args.receiver = Receiver(args.serverURL,
                             args.regAddr,
                             args.mode)
    args.model = Model(source=args.geometryImage,
                       target=args.floodRange,
                       mask=0.,
                       start=args.start,
                       startOnGrid=args.startOnGrid,
                       export=True)()
    args.emailSender = EmailSender(args.myGmail,
                                   args.myPW,
                                   args.addresses)
    args.thingspeakSender = ThingSpeakSender(args.writeApiKey,
                                             args.headers)

    receiver = args.receiver
    model = args.model
    emailSender = args.emailSender
    thingSpeakSender = args.thingspeakSender
    timezone = pytz.timezone(args.timezone)
    print("[Main] Finished initialization !")


def SaveHeightDataToCSV(file, height):
    """
    Save the flood height data received from the IoT device to a CSV file and Thinkspeak cloud:
    """

    # Save height data to a CSV file:
    now = datetime.datetime.now(timezone)
    date = f"{now.year}/{now.month}/{now.day}"
    clock = f"{now.hour}:{now.minute}:{now.second}"
    data = f"{date}, {clock}, {height}"
    print("\n"+"[Main] "+data+"(cm)")
    file.write(data+"\n")
    file.flush()

    # Save height data to Thinkspeak cloud:
    thingSpeakSender.PostToThingspeak(height)


def SaveMostNewNonNegativeHeightData(height):
    """
    Save most new non-negative flood height data to a JSON file:
    """

    with open(args.heightDataNew, "w") as f:
        json.dump({"MostNewHeightData": round(height, 3)}, f)
        f.flush()


def JudgeToSendEmail():
    """
    Judge whether need to send waring e-mail of the flood or not:
    """

    time.sleep(3)
    print("[Main] Start judging whether send e-mail or not !")
    sendTime = -1e100
    while True:
        currTime = time.time()
        if currTime - sendTime >= args.nextTimeInterval:
            height = receiver.height
            if height and height >= args.thresholds[0]:
                emailSender.SendFloodHeightMessages(f"絕望! 淹水已超過{height}公分!!")
                sendTime = currTime
            elif height and height >= args.thresholds[1]:
                emailSender.SendFloodHeightMessages(f"震驚! 淹水已超過{height}公分!!")
                sendTime = currTime
            elif height and height >= args.thresholds[2]:
                emailSender.SendFloodHeightMessages(f"注意! 淹水已超過{height}公分!!")
                sendTime = currTime

        time.sleep(10)


def ReceiveFloodHeight():
    """
    Receive the flood height data detected by the IoT device:
    """

    print("[Main] Start receiving height data !")
    receiver.ReceiveData(updateTime=args.updateTime)


def MakeFloodRangeImage():
    """
    Make images of the range of the flood:
    """

    time.sleep(4)
    print("[Main] Start making flood range image !\n"+"="*50+"\n")
    with open(args.heightData, "a") as f:
        oldHeight = -1e100
        while True:
            height = receiver.height
            if height is not None:
                SaveHeightDataToCSV(file=f,
                                    height=height)
                height = 0. if height <= 0. else height
                SaveMostNewNonNegativeHeightData(height)
                if abs(height-oldHeight) >= 0.01:
                    print("-------------Making Flood Range Image-------------")
                    model.Tune(height, export=True)
                    print("-"*50+'\n')
                    oldHeight = height
                else:
                    print("[Main] Needn't make a flood range image.")
            else:
                print("\n[Main] No data received ...\n")

            time.sleep(args.updateTime-0.205)


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

    if args.sendEmail:
        thread2 = threading.Thread(
            target=JudgeToSendEmail, name="JudgeToSendEmail")
        thread2.start()

    # Export coordinate data:
    coordinate = twd97_to_wgs84.GetLatLng()
    with open(args.coordinateData, "w") as f:
        json.dump(coordinate, f)

    print("[Main] Got the coordinate of monited range !")
