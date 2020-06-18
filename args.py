
def Init():
    """
    Initialize the basic arguments:
    """

    global serverURL, regAddr, updateTime, root, geometryImage, floodRange, heightData, heightDataNew, \
        coordinateData, start, startOnGrid, mode, timezone, receiver, model, emailSender, thingspeakSender, \
        sendEmail, myGmail, myPW, addresses, thresholds, placeName, nextTimeInterval, writeApiKey, headers

    # IoTtalk settings:
    serverURL = 'https://demo.iottalk.tw/'
    regAddr = '0511238'
    updateTime = 5
    mode = "test"

    # File settings:
    root = "./static/img/"
    geometryImage = root+"nctu_6m_TWD97.asc"
    floodRange = root+"flood_range.png"
    heightData = root+"flood_height.csv"
    heightDataNew = root+"flood_new_height.json"
    coordinateData = root+"coordinate.json"

    # Flood model setting:
    start = (249756.83, 2742377.07)
    startOnGrid = False

    # Time zone:
    timezone = "Asia/Taipei"

    # E-mail address setting:
    sendEmail = True
    myGmail = "ezioatiar@gmail.com"
    myPW = "scocuwtmjmybksvl"
    addresses = "my.txt"
    thresholds = [45, 7, 1]
    placeName = "工程二館"
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
