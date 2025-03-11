from enum import Enum

class TextType(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node):
        if node.text == self.text and node.text_type == self.text_type and node.url == self.url:
            return True
        
    def __repr__(self):
         return f"TextNode({self.text}, {self.text_type.value}, {self.url})"