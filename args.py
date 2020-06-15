
def Init():
    """
    Initialize the basic arguments:
    """

    global serverURL, regAddr, updateTime, root, geometryImage, floodRange, heightData, heightDataNew, \
        coordinateData, start, startOnGrid, mode, timezone, receiver, model, emailSender, thingspeakSender, \
        sendEmail, myGmail, myPW, addresses, thresholds, nextTimeInterval, writeApiKey, headers

    # IoTtalk settings:
    serverURL = 'https://demo.iottalk.tw/'
    regAddr = '0511238'
    updateTime = 600
    mode = "real"

    # File settings:
    root = "./static/img/"
    geometryImage = root+"nctu_6m_TWD97.asc"
    floodRange = root+"flood_range.png"
    heightData = root+"flood_height.csv"
    heightDataNew = root+"flood_new_height.json"
    coordinateData = root+"coordinate.json"

    # Flood model setting:
    start = (249712.1, 2742474.0)
    startOnGrid = False

    # Time zone:
    timezone = "Asia/Taipei"

    # E-mail address setting:
    sendEmail = True
    myGmail = "ezioatiar@gmail.com"
    myPW = "a8077606"
    addresses = "my.txt"
    thresholds = [5, 2, 0]
    nextTimeInterval = updateTime*6

    # Thingspeak setting:
    writeApiKey = "OO1DE1N7LT6WXE17"
    headers = {"Content-type": "application/x-www-form-urlencoded",
               "Accept": "text/plain"}

    # Main objects references:
    receiver = None
    model = None
    emailSender = None
    thingspeakSender = None
