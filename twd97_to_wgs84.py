import args
import pyproj


# Coordinate system: WGS84 is epsg:4326, TWD97_Zone121 is epsg:3826 .

global proj

proj = pyproj.Transformer.from_crs(3826, 4326)


def Transform(tx, ty):
    """
    For TDW97_Zone121(x, y) => WGS84(lat, lng):
    """

    latLng = proj.transform(tx, ty)

    return latLng


def GetLatLng():
    """
    Get the coordinate of the IoT device and monited area:
    """

    ncols = args.model.params["ncols"]
    nrows = args.model.params["nrows"]
    xll = args.model.params["xllcorner"]
    yll = args.model.params["yllcorner"]
    size = args.model.params["cellsize"]
    start = args.start

    xul = xll
    yul = yll+ncols*size

    xlr = xll+nrows*size
    ylr = yll

    ul = Transform(xul, yul)
    lr = Transform(xlr, ylr)
    if not args.startOnGrid:
        start = Transform(start[0], start[1])

    return {"UpperLeft": ul, "LowwerRight": lr, "Start": start, "UpdateTime": args.updateTime}
