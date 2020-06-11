import time
import random
from iottalk import DAN


class Receiver(object):
    """
    A class which can pull the data on IoTtalk after being instantiated:
    """

    def __init__(self, serverURL, regAddr):
        self.serverURL = serverURL
        self.regAddr = regAddr

        self.height = None
        self.stop = None
        self.profile = None

    def __repr__(self):
        site = super(Receiver, self).__repr__()

        return "\n"+"-"*50+"\n"+f"{site}\n"+'-'*50+f"\n{self.profile}"

    def ReceiveData(self, updateTime):
        DAN.profile['dm_name'] = 'FloodMoniter'
        DAN.profile['df_list'] = ['FloodHeightIn', 'FloodHeightOut']
        DAN.profile['d_name'] = 'FloodOutput'
        DAN.device_registration_with_retry(self.serverURL, self.regAddr)
        self.profile = DAN.profile
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
                    print('Reg_addr is not found. Try to re-register...')
                    DAN.device_registration_with_retry(
                        self.serverURL, self.regAddr)
                else:
                    print('Connection failed due to unknow reasons.')
                    time.sleep(1)

            time.sleep(updateTime)
