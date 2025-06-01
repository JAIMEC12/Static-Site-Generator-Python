from enum import Enum

class TextType(Enum):
    # Text node
    NORMAL_TEXT = "Normal Text"
    BOLD_TEXT = "**Bold Text**"
    ITALIC_TEXT = "_Italic Text_"
    CODE_TEXT = "`Code Text`"
    LINK_TEXT = "[anchor text](url)"
    IMAGES = "![alt text](url)"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
    
    def __eq__(self, value):
        return True if self.text == value.text and self.text_type == value.text_type and self.url == value.url else False

    def __repr__(self):
        return f"Text Node({self.text},{self.text_type.value},{self.url})"