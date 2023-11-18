from color import Color


class StylingPalette:
    def __init__(
        self,
        keywords=Color("#987dd2"),
        identifiers=Color("#ffffff"),
        literals=Color("#a8cd76"),
        operators=Color("#9cdbfb"),
        seperators=Color("#72a5cb"),
        comments=Color("#53597a"),
    ) -> None:
        self.keywords = keywords
        self.identifiers = identifiers
        self.literals = literals
        self.operators = operators
        self.seperators = seperators
        self.comments = comments
        self.whitespace = None
