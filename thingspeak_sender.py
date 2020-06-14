import time
import socket
import http.client
import urllib.parse


class ThingSpeakSender(object):
    """
    A class which can upload data to Thinkspeak cloud after being instantiated:
    """

    def __init__(self, writeApiKey, headers):
        self.writeApiKey = writeApiKey
        self.headers = headers
        self.conn = None
        self.isConnect = None
        self.response = None  # Seems to be times of data-uploading ...

        self.ConnectToCloud()

    def __repr__(self):
        site = super(ThingSpeakSender, self).__repr__()
        message = {"WriteApiKey": self.writeApiKey,
                   "Headers": self.headers,
                   "Connect": self.conn,
                   "UploadTimes": int(self.response)}

        return "\n"+"-"*50+"\n"+f"{site}\n"+'-'*50+f"\n{message}"

    def __del__(self):
        self.conn.close()
        print("[Thingspeak] Connection to Thinkspeak closed !")

    def ConnectToCloud(self):
        while (not self.isConnect):
            try:
                self.conn = http.client.HTTPConnection("api.thingspeak.com:80")
                self.conn.connect()
                self.isConnect = True
            except (http.client.HTTPException, socket.error) as e:
                print(f"Error! {e}\n")
                self.isConnect = False
                time.sleep(10)

    def PostToThingspeak(self, height):
        payload = urllib.parse.urlencode({'field1': height,
                                          'key': self.writeApiKey})
        self.conn.request("POST", "/update", payload, self.headers)
        try:
            response = self.conn.getresponse()
            self.response = response.read()
        except http.client.RemoteDisconnected:
            print("[Thingspeak] Didn't get response.")
