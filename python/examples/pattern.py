class SimplePattern:
    i = 0

    def __init__(self, colors):
        self.colors = colors

    def getColors(self):
        return self.colors

    def getColor(self, idx):
        return self.colors[(idx+self.i) % len(self.colors)]

    def setColors(self, colors):
        self.colors = colors

    def bump(self, bump_value=1):
        self.i += bump_value
