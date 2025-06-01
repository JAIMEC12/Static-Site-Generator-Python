from functools import reduce
from textnode import TextNode, TextType

class HTMLNode():
    def __init__ (self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        line = ""
        # After doing the project, I notice I can use reduce
        for props in self.props:
            line = line + f'{props}="{self.props[props]}" '
        #Other possible solutions
        # line = reduce(lambda acc, item: acc + f'{item}="{self.props[item]}" ',self.props,"")
        # line = "".join(f'{props}="{self.props[props]}" ' for props in self.props)
        return line.strip()
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        else:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self,tag,children, props=None):
        super().__init__(tag,None, children, props)
    
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("There is no tag specified")
        elif self.children == None:
            raise ValueError("There is no children")
        else:
            return f"<{self.tag} {self.props_to_html()}>{reduce(lambda acc, x: acc + x.to_html(), self.children, "")}</{self.tag}>"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL_TEXT:
            return LeafNode(None, value=text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK_TEXT:
            return LeafNode(tag="a", value=text_node.text, props={"alt": text_node.text, "href": text_node.url,})
        case TextType.IMAGES:
            return LeafNode(tag="img", value=text_node.text, props={"alt": text_node.text, "src": text_node.url,})      
        case _:
            raise Exception("invalid HTML:  incorrect type")