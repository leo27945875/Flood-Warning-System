import time
import random
from iottalk import DAN


class Receiver(object):
    """
    A class which can pull the data on IoTtalk after being instantiated:
    """

    def __init__(self, mode='real'):
        self.serverURL = 'https://demo.iottalk.tw/'
        self.regAddr = '0522238'
        self.mode = mode
        self.height = None

        if self.mode == 'real':
            self.ConnectToIoTtalk()

    def __del__(self):
        print("Connection to IoTtalk closed !")

    def ConnectToIoTtalk(self):
        DAN.profile['dm_name'] = 'FloodMoniter'
        DAN.profile['df_list'] = ['FloodHeightIn', 'FloodHeightOut']
        DAN.profile['d_name'] = 'FloodOutput_Linebot'
        DAN.device_registration_with_retry(self.serverURL, self.regAddr)
        self.profile = DAN.profile

    def ReceiveData(self):
        if self.mode == "real":
            try:
                ODF_data = DAN.pull('FloodHeightOut')
                if ODF_data != None:
                    self.height = ODF_data[0]
                    print('-'*50+f"\nheight = {self.height}(cm)\n"+'-'*50)
                else:
                    self.height = None
                    print('-'*50+'\n'+"No data received ...\n"+'-'*50)

            except Exception as e:
                print(e)
                if str(e).find('mac_addr not found:') != -1:
                    print('Reg_addr is not found. Try to re-register...')
                    DAN.device_registration_with_retry(
                        self.serverURL, self.regAddr)
                else:
                    print('Connection failed due to unknow reasons.')
                    time.sleep(1)

        elif self.mode == "test":
            self.height = random.randint(0, 5)
            print('-'*50+'\n'+f"height = {self.height}(cm)\n"+'-'*50)

        else:
            raise ValueError(
                "Argument 'mode' must be one of 'real' and 'test' .")
