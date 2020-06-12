import numpy as np
import os
from linecache import getline
from matplotlib.pyplot import imsave


class Model(object):
    """
    A class which can run flood-fill algorithm according to the height data received by receiver objects
    and geometry of the monited area after being instantiated:
    """

    def __init__(self, source, target, mask, start, startOnGrid, export=False):
        self.source = source
        self.target = target
        self.mask = mask
        self.start = start
        self.startOnGrid = startOnGrid
        self.export = export

        self.graph = None
        self.hdr = None
        self.wet = None
        self.flood = None
        self.params = None

    def __call__(self):
        self.LoadGraph()
        self.FindStart()
        self.MaskImage()
        self.FloodFillAlgorithm()
        self.Export()

        return self

    def __repr__(self):
        site = super(Model, self).__repr__()
        message = {"Input file": self.source,
                   "Output file": self.target,
                   "Is in terms of grid": self.startOnGrid,
                   "Start point": self.start,
                   **self.params}

        return "\n"+"-"*50+"\n"+f"{site}\n"+'-'*50+f"\n{message}"

    def LoadGraph(self):
        self.hdr = [getline(self.source, i) for i in range(1, 7)]
        self.params = {i.split()[0]: float(i.split()[1]) for i in self.hdr}
        self.params["ncols"] = int(self.params["ncols"])
        self.params["nrows"] = int(self.params["nrows"])
        try:
            self.params["NODATA_value"] = int(self.params["NODATA_value"])
        except KeyError:
            self.params["NODATA_value"] = None
            self.hdr.pop()
            self.skip = 5
        else:
            self.skip = 6
        finally:
            self.graph = np.loadtxt(self.source, skiprows=self.skip)
            print("Geometry image has been loaded !")

    def FindStart(self):
        if not self.startOnGrid:
            dx = self.start[0]-self.params["xllcorner"]
            dy = self.start[1]-self.params["yllcorner"]
            gx = int(dx/self.params["cellsize"])
            gy = self.graph.shape[0]-int(dy/self.params["cellsize"])-1
            self.start = (gx, gy)
            self.startOnGrid = True

    def MaskImage(self):
        self.wet = np.where(self.graph < self.mask +
                            self.graph[self.start[1], self.start[0]], 1, 0)
        print("Image masked.")

    def FloodFillAlgorithm(self):
        if self.startOnGrid:
            c = self.start[0]
            r = self.start[1]
            wet = self.wet

            filled = set()
            fill = set()
            fill.add((c, r))
            width = wet.shape[1]-1
            height = wet.shape[0]-1
            flood = np.zeros_like(wet, dtype=np.int8)

            print("Beginning flood fill algorithm.")
            while fill:
                x, y = fill.pop()

                if (y == height
                    or x == width
                    or x < 0
                    or y < 0
                        or self.graph[y][x] == self.params["NODATA_value"]):

                    continue

                if wet[y][x] == 1:
                    flood[y][x] = 1
                    filled.add((x, y))

                    west = (x-1, y)
                    east = (x+1, y)
                    north = (x, y-1)
                    south = (x, y+1)
                    if not west in filled:
                        fill.add(west)
                    if not east in filled:
                        fill.add(east)
                    if not north in filled:
                        fill.add(north)
                    if not south in filled:
                        fill.add(south)

            self.flood = flood
            self.wet = None
            print("Finished Flood fill.")
        else:
            raise Exception(
                "Can't calculate the flood, because self.startOnGrid is False!")

    def Export(self):
        if self.export:
            fileExt = os.path.splitext(self.target)[-1]
            if fileExt == ".asc":
                print("Saving image as .asc ...")
                header = ""
                for i in range(self.skip):
                    header += self.hdr[i]

                with open(self.target, "wb") as f:
                    f.write(bytes(header, "UTF-8"))
                    np.savetxt(f, self.flood, fmt="%1i")

            elif fileExt == ".png":
                print("Saving image as .png ...")
                r = np.ones(
                    [self.params["nrows"], self.params["ncols"]])*0.047058823529411764
                g = np.ones(
                    [self.params["nrows"], self.params["ncols"]])*0.615686274509804
                b = self.flood
                a = self.flood*0.7
                imsave(self.target, np.stack([r, g, b, a], axis=-1))
        else:
            print("Didn't save any image !")

        print("Done!")

    def Tune(self, newMask, export=False):
        print("Recompute the flood range ...")
        self.mask = newMask
        self.export = export
        self.MaskImage()
        self.FloodFillAlgorithm()
        self.Export()
