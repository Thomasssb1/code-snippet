import json
from color import Color


class configFile:
    def __init__(
        self,
        filepath: str,
    ) -> None:
        with open(filepath, "r") as f:
            data = json.loads(f.read())
            self.language = next(iter(data))
            self.show_errors = data[self.language]["showErrors"]
            self.remove_comments = data[self.language]["showComments"]
            self.keyword = Color(data[self.language]["style"]["keywords"])
            self.identifier = Color(data[self.language]["style"]["identifiers"])
            self.operator = Color(data[self.language]["style"]["operators"])
            self.seperator = Color(data[self.language]["style"]["seperators"])
            self.comment = Color(data[self.language]["style"]["comments"])
            self.background = Color(data[self.language]["style"]["background"])
            self.literal = literal(data[self.language]["style"]["literals"])


class literal:
    def __init__(
        self,
        identifiers,
    ) -> None:
        self.string = Color(identifiers["string"])
        self.number = Color(identifiers["number"])
