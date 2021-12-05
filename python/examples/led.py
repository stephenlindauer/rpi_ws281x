class LED:
    def __init__(self, strip, id, lightIdx, x, y):
        self.xPos = x
        self.yPos = y
        self.next = []
        self.previous = []
        self.lightIdx = lightIdx
        self.strip = strip
        self.id = id

    def addNext(self, nextLed):
        self.next.append(nextLed)
        # Add circular link
        if self not in nextLed.previous:
            nextLed.addPrevious(self)

    def addPrevious(self, previousLed):
        self.previous.append(previousLed)
        # Add circular link
        if self not in previousLed.next:
            previousLed.addNext(self)

    def setColor(self, color):
        self.strip.setPixelColor(self.lightIdx, color)

    def serialize(self):
        return {
            "id": self.id,
            "xPos": self.xPos,
            "yPos": self.yPos,
            "lightIdx": self.lightIdx,
            "stripIdx": 0,
            "next": list(map(lambda n: n.id, self.next))
        }
