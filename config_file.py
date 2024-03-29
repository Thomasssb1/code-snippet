import json
from color import Color


class configFile:
    """
    This class is used to parse the config file.
    """

    def __init__(
        self,
        filepath: str,
        *args,
    ) -> None:
        """
        This function is used to parse the config file.

        You can define a language to be used by passing it as an argument, otherwise it will be determined automatically.
        """
        with open(filepath, "r") as f:
            data = json.loads(f.read())
            if args:
                self.language = args[0]

            else:
                self.language = next(iter(data))
            self.show_errors = data[self.language]["showErrors"]
            self.remove_comments = data[self.language]["showComments"]
            self.keyword = Color(data[self.language]["style"]["keywords"])
            self.identifier = Color(data[self.language]["style"]["identifiers"])
            self.operator = Color(data[self.language]["style"]["operators"])
            self.seperator = Color(data[self.language]["style"]["seperators"])
            self.comment = Color(data[self.language]["style"]["comments"])
            self.background = Color(data[self.language]["style"]["background"])
            self.literal = type(
                "literal",
                (),
                {
                    "string": Color(data[self.language]["style"]["literals"]["string"]),
                    "number": Color(data[self.language]["style"]["literals"]["number"]),
                },
            )
