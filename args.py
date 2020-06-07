
def Init():

    global serverURL, regAddr, geometryImage, floodRange, start, startOnGrid, receiver, model

    serverURL = 'https://demo.iottalk.tw/'
    regAddr = '0511238'
    geometryImage = "./data/nctu_6m_TWD97.asc"
    floodRange = "./data/flood_range.png"
    start = (249712.1, 2742474.0)
    startOnGrid = False
    receiver = None
    model = None
