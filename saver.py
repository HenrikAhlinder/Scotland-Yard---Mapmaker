"""Module designed to save and load maps created."""


class Savefilemaker():
    def __init__(self, gridsize):
        self.tempfile = open(".temp.dat", "w")  # Wipe the temporary savefile.
        self.gridsize = gridsize    # Tuple (width, height)
        self.stopsize = 0
        self.stops = {
                "taxi"      :[],
                "bus"       :[],
                "underground"   :[],
                "both"          :[],}
        self.lines = {
                "taxilines"         :[],
                "buslines"          :[],
                "undergroundlines"  :[]}


    def add_stop(self, stoptype, coordinates, stopsize):
        """Saves the coordinate and stoptype."""
        self.stops[stoptype].append(coordinates)
        self.stopsize = stopsize

    def add_line(self, linetype, coordinates):
        self.lines[linetype].append(coordinates)

    def reset(self, gridsize, stopsize):
        """Called when gridsize is changed, resets the map."""
        self.stops = {}
        self.lines = {}
        self.gridsize = gridsize
        self.stopsize = stopsize


    def save(self):
        """Save the currently loaded map into a savefile."""
        pass


    def load(self, filename):
        """Load the data from the file into the current map."""
        return ("taxi", self.stops["taxi"][0], self.stopsize)
