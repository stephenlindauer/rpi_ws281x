class Program():
    name = ""
    system = None
    program_range = None

    def __init__(self, name, program_range=None):
        self.name = name
        self.program_range = program_range

    def registerSystem(self, system):
        self.system = system

    def update(self):
        pass

    def paint(self, color, lightRange=None):
        if (lightRange and self.program_range):
            # find intersections
            intersection = range(
                max(lightRange[0], self.program_range[0]),
                min(lightRange[-1], self.program_range[-1])+1)
            if (intersection.stop-intersection.start > 0):
                self.system.paint(color, intersection)

            # print(intersection)

            pass
        elif (self.program_range):
            # print("use program range")
            # No range provided to paint(), use program
            self.system.paint(color, self.program_range)
        else:
            # print("use lightRange (default)")
            # No program_range or no ranges at all, paint it all
            self.system.paint(color, lightRange)
