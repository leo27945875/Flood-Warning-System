from flood_model import Model
from auto_email_sender import EmailSender
import args
import time

args.Init()
# model = Model(source=args.coordinateImage,
#               target=args.floodRange,
#               mask=0.,
#               start=args.start,
#               startOnGrid=args.startOnGrid,
#               export=True)()

# startT = time.time()
# model.Tune(5)
# d = time.time()-startT
# print(d)

sender = EmailSender(args.myGmail, args.myPW, args.addresses)
startT = time.time()
sender.SendFloodHeightMessages("AAAAAAAAAAAA")
d = time.time()-startT
print(d)
