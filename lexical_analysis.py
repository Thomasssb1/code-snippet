import re
import json
from config_file import configFile

"""
Keywords
Identifiers
Literals
Operators
Seperators
Comments
Whitespaces
"""

with open("config/java.json", "r") as f:
    data = json.loads(f.read())
    KEYWORDS = data["keywords"]
    INDENTIFIER = r"[a-zA-Z_][a-zA-Z0-9_]*"
    OPERATORS = data["operators"]
    SEPERATORS = data["seperators"]
    STRING_CHAR = "\"|'"


class LexicalAnalysis:
    def __init__(self, code: str, config: configFile) -> None:
        self.code = code
        self.config = config
        self.tokens = []

    def preprocess(self, code: str = None, between_lines: tuple = (1,)) -> str:
        if code is None:
            code = self.code
        code = removeBlockComments(code).splitlines()
        between_lines = (
            between_lines[0] if len(between_lines) > 0 else 1,
            between_lines[1] if len(between_lines) > 1 else len(code),
        )
        print(between_lines)
        code = code[between_lines[0] - 1 : between_lines[1]]
        for i, line in enumerate(code):
            code[i] = removeComments(line, self.config.line_comment)
        return "\n".join(filter(None, code))

    def tokenisation(self, cleaned_code: str) -> list:
        tokens = []
        is_string = False
        split_pattern = createSeperatorRegex()
        create_string = []
        for word in re.split(split_pattern, cleaned_code):
            if not word:
                pass

            if is_string:
                create_string.append(word)
            elif re.match("\s+", word):
                tokens.append(("whitespace", word))
                pass

            for _ in range(0, len(re.findall(STRING_CHAR, word))):
                is_string = not is_string
                if is_string:
                    create_string.append(word)
                elif create_string:
                    tokens.append(("literal", " ".join(create_string)))
                    create_string = []
                    is_string = False
                    pass

            if word in KEYWORDS:
                tokens.append(("keyword", word))
            elif word in SEPERATORS:
                tokens.append(("seperator", word))
            elif word in OPERATORS:
                tokens.append(("operator", word))
            else:
                identifier = True if re.fullmatch(INDENTIFIER, word) else False
                if identifier and not is_string:
                    tokens.append(("identifier", word))

        print(f"tokens: {tokens}")
        return tokens


# Need to update to work for different block comments
def removeBlockComments(code: str) -> str:
    return re.sub("\/\*([\s\S]*?)\*\/", "", code)


def removeComments(code: str, comment_type: str) -> str:
    no_string = removeString(code)
    comment_split = no_string.strip().rpartition(comment_type)
    try:
        comment_position = comment_split.index(comment_type)
    except:
        comment_position = 3
    comment = "".join(list(comment_split[comment_position::]))
    return code.replace(comment, "").rstrip()


def removeString(code: str) -> str:
    return re.sub(r"""(\"|')([\s\S]*?)(\"|')""", "", code)


def createSeperatorRegex() -> str:
    temp = ["\\" + sep for sep in SEPERATORS + ["s+"]]
    return f"({'|'.join(temp)})"
