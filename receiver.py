import time
import random
from iottalk import DAN


class Receiver(object):
    """
    A class which can pull the data on IoTtalk after being instantiated:
    """

    def __init__(self, serverURL, regAddr, mode):
        self.serverURL = serverURL
        self.regAddr = regAddr
        self.mode = mode
        self.height = None
        self.stop = None
        self.profile = None

        if mode == 'real':
            self.ConnectToIoTtalk()

    def __repr__(self):
        site = super(Receiver, self).__repr__()

        return "\n"+"-"*50+"\n"+f"{site}\n"+'-'*50+f"\n{self.profile}"

    def __del__(self):
        print("[IoTtalk] Connection to IoTtalk closed !")

    def ConnectToIoTtalk(self):
        DAN.profile['dm_name'] = 'FloodMoniter'
        DAN.profile['df_list'] = ['FloodHeightIn', 'FloodHeightOut']
        DAN.profile['d_name'] = 'FloodOutput'
        DAN.device_registration_with_retry(self.serverURL, self.regAddr)
        self.profile = DAN.profile
        self.mode = 'real'

    def ReceiveData(self, updateTime):
        if self.mode == "real":
            self.stop = True
            while True:
                try:
                    ODF_data = DAN.pull('FloodHeightOut')
                    if ODF_data != None:
                        self.height = ODF_data[0]
                        self.stop = False
                    else:
                        self.height = None
                        self.stop = True

                except Exception as e:
                    print(e)
                    if str(e).find('mac_addr not found:') != -1:
                        print(
                            '[IoTtalk] Reg_addr is not found. Try to re-register...')
                        DAN.device_registration_with_retry(
                            self.serverURL, self.regAddr)
                    else:
                        print('[IoTtalk] Connection failed due to unknow reasons.')
                        time.sleep(1)

                time.sleep(updateTime)

        elif self.mode == "test":
            self.stop = False
            while True:
                self.height = random.randint(0, 5)
                time.sleep(updateTime)

        else:
            raise ValueError(
                "[IoTtalk] Argument 'mode' must be one of 'real' and 'test' .")
