"""Module designed to save and load maps created."""
import json
from datetime import datetime

class Savefilemaker():
    def __init__(self, gridsize):
        self.tempfile = open(".temp.dat", "w")  # Wipe the temporary savefile.
        self.gridsize = gridsize    # Tuple (width, height)
        self.stopsize = 0
        self.stops = {
                "taxi"      :[],
                "busstop"       :[],
                "underground"   :[],
                "both"          :[],}
        self.lines = {
                "taxiline"         :[],
                "busline"          :[],
                "undergroundline"  :[]}


    def add_stop(self, stoptype, coordinates, stopsize):
        """Saves the coordinate and stoptype."""
        self.stops[stoptype].append(coordinates)
        self.stopsize = stopsize

    def remove_stop(self, coordinates):
        """Remove the stop from the saved list."""
        for coord_list in self.stops.values():
            if coordinates in coord_list:
                coord_list.remove(coordinates)

    def add_line(self, linetype, coordinates):
        self.lines[linetype].append(coordinates)

    def remove_line(self, coordinates):
        """Remove a line from savefile."""
        for linetype in self.lines:
            if coordinates in self.lines[linetype]:
                self.lines[linetype].remove(coordinates)

    def reset(self, gridsize):
        """Called when gridsize is changed, resets the map."""
        self.stops = {
                "taxi"      :[],
                "busstop"       :[],
                "underground"   :[],
                "both"          :[],}
        self.lines = {
                "taxiline"         :[],
                "busline"          :[],
                "undergroundline"  :[]}
        self.gridsize = gridsize
        self.stopsize = 0

    def save(self, file):
        """Save the currently loaded map into a savefile."""
        jsondump = {
                "stops":self.stops,
                "lines":self.lines,
                "gridsize":self.gridsize,
                "stopsize":self.stopsize}

        file.write(json.dumps(jsondump))

    def load(self, filename):
        """Load the data from the file into the current map."""
        data = json.loads(open(filename, "r").read())
        self.gridsize = data['gridsize']
        self.stopsize = data['stopsize']
        self.stops    = data['stops']
        self.lines    = data['lines']

        return {
                "gridsize":self.gridsize,
                "stops": self.stops,
                "lines": self.lines,
                "stopsize":self.stopsize}
