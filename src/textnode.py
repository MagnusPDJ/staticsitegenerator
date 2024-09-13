from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other):
        return (self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.text_type_text.value:
            return LeafNode(None, text_node.text)
        case TextType.text_type_bold.value:
            return LeafNode("b", text_node.text)
        case TextType.text_type_italic.value:
            return LeafNode("i", text_node.text)
        case TextType.text_type_code.value:
            return LeafNode("code", text_node.text)
        case TextType.text_type_link.value:
            return LeafNode("a", text_node.text)
        case TextType.text_type_image.value:
            return LeafNode("img", "", {"src": text_node.url,"alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        nodes = []
        slices = old_node.text.split(delimiter)
        if len(slices) % 2 == 0:
            raise Exception("Invalid Markdown syntax: miss matching delimiters")               
        for i in range(len(slices)):
            if  slices[i] == "":
                continue
            if (i+1) % 2 != 0:
                nodes.append(TextNode(slices[i], "text"))
            else:
                nodes.append(TextNode(slices[i], text_type))
        new_nodes.extend(nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall( r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall( r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        nodes = []
        text_to_slice = old_node.text
        images = extract_markdown_images(old_node.text)
        images_count = len(images)
        if images_count == 0:
            new_nodes.append(old_node)
            continue            
        for i in range(images_count):
            slices = text_to_slice.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if len(slices) != 2:
                raise ValueError("Invalid Markdown syntax, image is not closed")
            if  slices[0] == "":
                nodes.append(TextNode(images[i][0], "image", images[i][1]))
                text_to_slice = slices[1]
                continue
            nodes.append(TextNode(slices[0], "text"))
            nodes.append(TextNode(images[i][0], "image", images[i][1]))
            text_to_slice = slices[1]
        if text_to_slice != "":
            nodes.append(TextNode(text_to_slice, "text"))
        new_nodes.extend(nodes)    
        return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != "text":
            new_nodes.append(old_node)
            continue
        nodes = []
        text_to_slice = old_node.text
        links = extract_markdown_links(old_node.text)
        links_count = len(links)
        if links_count == 0:
            new_nodes.append(old_node)
            continue 
        for i in range(links_count):
            slices = text_to_slice.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if len(slices) != 2:
                raise ValueError("Invalid Markdown syntax, link is not closed")
            if  slices[0] == "":
                nodes.append(TextNode(links[i][0], "link", links[i][1]))
                text_to_slice = slices[1]
                continue
            nodes.append(TextNode(slices[0], "text"))
            nodes.append(TextNode(links[i][0], "link", links[i][1]))
            text_to_slice = slices[1]
        if text_to_slice != "":
            nodes.append(TextNode(text_to_slice, "text"))
        new_nodes.extend(nodes)    
        return new_nodes

def text_to_textnodes(text):
    text_to_split = [TextNode(text, "text")]
    textnodes = split_nodes_image(text_to_split)
    textnodes = split_nodes_link(textnodes)
    textnodes = split_nodes_delimiter(textnodes, "**", "bold")
    textnodes = split_nodes_delimiter(textnodes, "`", "code")
    textnodes = split_nodes_delimiter(textnodes, "*", "italic")
    return textnodes

def markdown_to_blocks(markdown):
    block_list = []
    split_markdown = markdown.split("\n\n")
    for split in split_markdown:
        if split == "":
            continue
        block_list.append(split.strip())
    
    return block_list

def block_to_block_type(block):
    lines = block.split("\n")
    if (
        block.startswith("######")
        or block.startswith("#####")
        or block.startswith("####")
        or block.startswith("###")
        or block.startswith("##")
        or block.startswith("#")
    ):
        return "heading"
    if len(lines) > 2 and block[:3] =="```" and block[-3:] == "```":
        return "code"   
    if block[:1] == ">":
        for line in lines:
            if line[:1] != ">":
                return "paragraph"
        return "quote"
    if block[:2] == "* ":
        for line in lines:
            if line[:2] != "* ":
                return "paragraph"
        return "unordered_list"
    if block[:2] == "- ":
        for line in lines:
            if line[:2] != "- ":
                return "paragraph"
        return "unordered_list"
    if block[:3] == "1. ":
        i = 1
        for line in lines:
            if line[:3] != f"{i}. ":
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"