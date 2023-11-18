class Color:
    def __init__(self, color: str) -> None:
        if self.setColor(color) == True:
            self.color = color

    def setColor(self, color: str) -> bool:
        if self.color[0] == "#":
            return True
        elif color.count(",") == 3:
            return True
        else:
            raise TypeError
