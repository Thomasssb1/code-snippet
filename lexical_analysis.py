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
    COMMENTS = data["comments"]


class LexicalAnalysis:
    def __init__(self, code: str, config: configFile) -> None:
        self.code = code
        self.config = config
        self.tokens = []

    def preprocess(self, between_lines: tuple, code: str = None) -> str:
        if code is None:
            code = self.code
        code = removeBlockComments(code).splitlines()
        between_lines = (
            between_lines[0] if len(between_lines) > 0 else 1,
            between_lines[1] if len(between_lines) > 1 else len(code),
        )
        code = code[between_lines[0] - 1 : between_lines[1]]
        for i, line in enumerate(code):
            code[i] = removeComments(line, COMMENTS["single"])
        return "\n".join(filter(None, code))

    def tokenisation(self, cleaned_code: str, config: configFile) -> list:
        tokens = []
        is_string = False
        split_pattern = createSeperatorRegex()
        create_string = []
        for word in re.split(split_pattern, cleaned_code):
            if not word:
                continue

            if is_string:
                create_string.append(word)
            elif re.match("\s+", word):
                tokens.append(("whitespace", word))
                continue

            quoted_count = len(re.findall(STRING_CHAR, word))
            for _ in range(0, quoted_count):
                is_string = not is_string
                if is_string:
                    create_string.append(word)
                elif create_string:
                    tokens.append((config.literal.string, "".join(create_string)))
                    create_string = []
                    is_string = False
            if quoted_count > 0:
                continue

            if word in KEYWORDS:
                tokens.append((config.keyword, word))
            elif word in SEPERATORS:
                tokens.append((config.seperator, word))
            elif word in OPERATORS:
                tokens.append((config.operator, word))
            else:
                identifier = True if re.fullmatch(INDENTIFIER, word) else False
                if identifier and not is_string:
                    tokens.append((config.identifier, word))
                elif not is_string:
                    if word.isdigit():
                        tokens.append((config.literal.number, word))
                    else:
                        for char in word:
                            if char.isdigit():
                                tokens.append((config.literal.number, char))
                            else:
                                tokens.append((config.operator, char))

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
