import re
from config_file import configFile
class LexicalAnalysis:
    def __init__(self, code:str, config:configFile) -> None:
        self.code = code
        self.config = config

    def preprocess(self, code:str = None, between_lines:tuple = (1,)) -> str:
        if code is None:
            code = self.code
        code = removeBlockComments(code).splitlines()
        between_lines = (between_lines[0] if len(between_lines) > 0 else 1, between_lines[1] if len(between_lines) > 1 else len(code))
        print(between_lines)
        code = code[between_lines[0]-1:between_lines[1]]
        for i, line in enumerate(code):
            code[i] = removeComments(line, self.config.line_comment)
        return "\n".join(filter(None, code))
        
    
# Need to update to work for different block comments
def removeBlockComments(code:str) -> str:
    return re.sub("\/\*([\s\S]*?)\*\/", "", code)

def removeComments(code:str, comment_type:str) -> str:
    no_string = removeString(code)
    comment_split = no_string.strip().rpartition(comment_type)
    try:
        comment_position = comment_split.index(comment_type);
    except:
        comment_position = 3
    comment = "".join(list(comment_split[comment_position::]))
    return code.replace(comment, "").rstrip()

def removeString(code:str) -> str:
    return re.sub(r"""(\"|')([\s\S]*?)(\"|')""", "", code)
