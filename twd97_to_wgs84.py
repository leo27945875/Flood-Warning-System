import args
from pyreproj import Reprojector


# Coordinate system: WGS84 => 4326, TWD97_Zone121 => 3826 .
rp = Reprojector()
Func = rp.get_transformation_function(3826, 4326)


def Transform(tx, ty):
    latLng = list(Func(tx, ty))

    return latLng


def GetLatLng():
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

    return {"UpperLeft": ul, "LowwerRight": lr, "Start": start}
