import json
class configFile:
    def __init__(self, filepath:str) -> None:
        with open(filepath, "r") as f:
            data = json.loads(f.read())
            self.language = next(iter(data))
            self.show_errors = data[self.language]["showErrors"]
            self.line_comment = data[self.language]["commentConfig"]["lineComment"]
            self.block_comment = data[self.language]["commentConfig"]["blockComment"]
            self.remove_comments = data[self.language]["commentConfig"]["removeComments"]
            