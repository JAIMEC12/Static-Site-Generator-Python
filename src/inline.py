from textnode import TextType, TextNode
import re

def split_node_delimiter(old_nodes, delimiter, text_type):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL_TEXT:
            node_list.append(node) 
            continue
        elif delimiter in node.text:
            line_splitted = node.text.split(f'{delimiter}')
            node_list.extend(
                [TextNode(line_splitted[x], TextType.NORMAL_TEXT if x%2 == 0 else text_type) for x in range(0,len(line_splitted))]
            )
        else:
            node_list.append(node)
    return node_list


def extract_markdown_images(text):
    # match = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return match

def split_nodes_image(old_nodes):
    new_list = []
    for node in old_nodes:
        words_to_split = extract_markdown_images(node.text)
        if len(words_to_split) == 0 or node.text_type != TextType.NORMAL_TEXT:
            new_list.append(node)
        else:
            originial_text = node.text
            before = ""
            for word in words_to_split:
                after = originial_text.split(f"![{word[0]}]({word[1]})",1)
                
                if len(after) != 2:
                    raise ValueError("No closure for formattee")
                before = after[0]

                if before != "":
                    new_list.append(TextNode(before,TextType.NORMAL_TEXT))
                
                new_list.append(TextNode(word[0],TextType.IMAGES,word[1]))
                originial_text = after[1]
            
            if originial_text != "":
                new_list.append(TextNode(originial_text,TextType.NORMAL_TEXT))
    
    return new_list

def split_nodes_link(old_nodes):
    new_list = []
    for node in old_nodes:
        words_to_split = extract_markdown_links(node.text)
        if len(words_to_split) == 0 or node.text_type != TextType.NORMAL_TEXT:
            new_list.append(node)
        else:
            original_text = node.text
            before = ""
            for word in words_to_split:
                after = original_text.split(f"[{word[0]}]({word[1]})",1)
                if len(after) != 2:
                    raise ValueError("No closure for formatee")
                before = after[0]
                if before != "":
                    new_list.append(TextNode(before,TextType.NORMAL_TEXT))
                new_list.append(TextNode(word[0],TextType.LINK_TEXT,word[1]))
                original_text = after[1]
            if original_text != "":
                new_list.append(TextNode(original_text,TextType.NORMAL_TEXT))
    return new_list



def text_to_text_node(text):
    list_textnode_bold = split_node_delimiter([TextNode(text, TextType.NORMAL_TEXT)],'**', TextType.BOLD_TEXT)
    list_textnode_italic = split_node_delimiter(list_textnode_bold,"_",TextType.ITALIC_TEXT)
    list_textnode_code = split_node_delimiter(list_textnode_italic,"`",TextType.CODE_TEXT)
    list_textnode_image = split_nodes_image(list_textnode_code)
    list_textnode_final = split_nodes_link(list_textnode_image)
    return list_textnode_final