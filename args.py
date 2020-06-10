
def Init():

    global serverURL, regAddr, updateTime, root, coordinateImage, floodRange, heightData, start, startOnGrid, receiver, model, mode, timezone

    # IoTtalk settings:
    serverURL = 'https://demo.iottalk.tw/'
    regAddr = '0511238'
    updateTime = 5.

    # File settings:
    root = "./static/img/"
    coordinateImage = root+"nctu_6m_TWD97.asc"
    floodRange = root+"flood_range.png"
    heightData = root+"flood_height.csv"

    # Flood model setting:
    start = (249712.1, 2742474.0)
    startOnGrid = False

    # Other settiings:
    mode = "test"
    timezone = "Asia/Taipei"

    # Main objects references:
    receiver = None
    model = None
