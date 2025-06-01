import enum
import re 
from htmlnode import ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
import inline

class BlockType(enum.Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST= "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    blocks_no_space = list(map(lambda x: x.strip(),blocks))
    return list(filter(lambda x: x!='',blocks_no_space))

def markdown_to_html_node(markdown):
    markdown_blocks= markdown_to_blocks(markdown)
    list_blocks = []
    for block in markdown_blocks:
        block__type = block_to_block_type(block)
        list_blocks.append(create_html_node(block,block__type))
    return ParentNode("div",list_blocks)


def text_to_children(text):
    childrens = []
    text_nodes = inline.text_to_text_node(text)
    for text_node in text_nodes: 
        childrens.append(text_node_to_html_node(text_node))
    return childrens


def create_html_node(block_text,block_type):
    match block_type:
        
        case BlockType.HEADING:
            formatee_text = block_text.replace("\n"," ") 
            return ParentNode(f"h{block_text.count("#")}",text_to_children(formatee_text))
        
        case BlockType.CODE:
            formatee_text = block_text.replace("```","")
            return ParentNode(f"pre",[text_node_to_html_node(TextNode(formatee_text.lstrip("\n"),TextType.CODE_TEXT))])
        
        case BlockType.QUOTE:
            formatee_text = block_text.replace(">","") 
            return ParentNode("blockquote", text_to_children(formatee_text))
        
        case BlockType.UNORDERED_LIST:
            formatee_text = block_text.replace("- ","",1)
            item_list = [ParentNode("li",text_to_children(re.sub(r"^\-\s","",line))) for line in block_text.split("\n")]
            return ParentNode("ul", item_list)
        
        case BlockType.ORDERED_LIST:
            item_list = [ParentNode("li",text_to_children(re.sub(r"^\d\.\s","",line))) for line in block_text.split("\n")]
            return ParentNode("ol", item_list)
        
        case BlockType.PARAGRAPH:
            formatee_text = block_text.replace("\n"," ") 
            return ParentNode("p",text_to_children(formatee_text))
        
        case _:
            raise Exception("Invalid BlockType: It does not exist")


def block_to_block_type(markdown):

    lines = markdown.split("\n")
    
    if re.match(r"^#{1,6} ", markdown):
        return BlockType.HEADING
    
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    
    if (all(line[0].isdigit() and line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1))):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH

    













    # if re.findall(r"^#{0,6} ", markdown):
    #     return BlockType.HEADING
    
    # elif markdown[0:3] == "```" and markdown[len(markdown)-3:len(markdown)] == "```":
    #     return BlockType.CODE
    
    # elif len(list((filter(lambda x: x[0] == ">", markdown.split("\n"))))) == len(markdown.split("\n")):
    #     return BlockType.QUOTE
    
    # elif len(list((filter(lambda x: x[0:2] == "- ", markdown.split("\n"))))) == len(markdown.split("\n")):
    #     return BlockType.UNORDERED_LIST
    
    # elif len(list(filter(lambda x: x[1:3] == ". ", markdown.split("\n")))) == len(markdown.split("\n")) and [x[0] for x in markdown.split("\n")] == [f"{x}" for x in range(1,len(markdown.split("\n"))+1)]:
    #     return BlockType.ORDERED_LIST
   
    # else:
    #     return BlockType.PARAGRAPH



    #Another solution for every line for ordered list
    # # elif re.findall("^\d\. ",markdown) and [x[0] for x in markdown.split("\n")] == [f"{x}" for x in range(1,len(markdown.split("\n"))+1)]:
    #     return BlockType.ORDERED_LIST