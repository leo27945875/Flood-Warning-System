
def Init():
    """
    Initialize the basic arguments:
    """

    global serverURL, regAddr, updateTime, root, coordinateImage, floodRange, \
        heightData, start, startOnGrid, mode, timezone, receiver, model, sender, \
        myGmail, myPW, addresses, thresholds, nextTimeInterval

    # IoTtalk settings:
    serverURL = 'https://demo.iottalk.tw/'
    regAddr = '0511238'
    updateTime = 5
    mode = "test"

    # File settings:
    root = "./static/img/"
    coordinateImage = root+"nctu_6m_TWD97.asc"
    floodRange = root+"flood_range.png"
    heightData = root+"flood_height.csv"

    # Flood model setting:
    start = (249712.1, 2742474.0)
    startOnGrid = False

    # Time zone:
    timezone = "Asia/Taipei"

    # Main objects references:
    receiver = None
    model = None
    sender = None

    # E-mail address setting:
    myGmail = "ezioatiar@gmail.com"
    myPW = "a8077606"
    addresses = "my.txt"
    thresholds = [5, 2, 0]
    nextTimeInterval = 20
