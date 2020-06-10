
def Init():

    global serverURL, regAddr, updateTime, root, coordinateImage, floodRange, heightData, start, startOnGrid, receiver, model, mode, timezone

    serverURL = 'https://demo.iottalk.tw/'
    regAddr = '0511238'
    updateTime = 5.
    root = "./static/img/"
    coordinateImage = root+"nctu_6m_TWD97.asc"
    floodRange = root+"flood_range.png"
    heightData = root+"flood_height.csv"
    start = (249712.1, 2742474.0)
    startOnGrid = False
    receiver = None
    model = None
    mode = "test"
    timezone = "Asia/Taipei"
