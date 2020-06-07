import math
import args


def Transform(ty, tx):
    lat = ty * 0.00000899823754
    lng = 121 + ((tx - 250000) * 0.000008983152841195214 /
                 math.cos(math.radians(lat)))

    return [lat, lng]


def GetLatLng():
    ncols = args.model.params["ncols"]
    nrows = args.model.params["nrows"]
    yll = args.model.params["yllcorner"]
    xll = args.model.params["xllcorner"]
    size = args.model.params["cellsize"]
    start = args.start

    yul = yll+ncols*size
    xul = xll

    ylr = yll
    xlr = xll+nrows*size

    ul = Transform(yul, xul)
    lr = Transform(ylr, xlr)
    if not args.startOnGrid:
        start = Transform(start[1], start[0])

    return {"UpperLeft": ul, "LowwerRight": lr, "Start": start}
