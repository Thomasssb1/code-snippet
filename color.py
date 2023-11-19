class ValueTooHigh(Exception):
    def __init__(self) -> None:
        message = "Value entered is greater than 255."
        super().__init__(message)


class InvalidColorType(Exception):
    def __init__(self) -> None:
        message = (
            "You can only use hexadecimal or rgb values to update the color attribute."
        )
        super().__init__(message)


class Color:
    def __init__(self, color: str) -> None:
        if self.setColor(color) == True:
            self.color = color
            self.hex = {10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}

    def setColor(self, color: str) -> bool:
        if color[0] == "#":
            return True
        elif color.count(",") == 2:
            r, g, b = color.split(",")[:3]
            if int(r) > 255 or int(g) > 255 or int(b) > 255:
                raise ValueTooHigh
            rgb = [
                item
                for sublist in [[int(v) // 16, int(v) % 16] for v in [r, g, b]]
                for item in sublist
            ]
            hexadecimal = ""
            for value in rgb:
                try:
                    hexadecimal += self.hex[value]
                except:
                    hexadecimal += str(value)
            print(hexadecimal)
        else:
            raise InvalidColorType
