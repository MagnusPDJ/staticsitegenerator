from enum import Enum
from htmlnode import LeafNode

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
        else:
            index = old_node.text.find(delimiter)
            if index == -1:
                new_nodes.append(old_node)
            else:
                nodes = []
                delimiter_count = old_node.text.count(delimiter)
                if delimiter_count < 2 or delimiter_count % 2 != 0:
                    raise Exception("Invalid Markdown syntax: miss matching delimiters")
                
                slices = old_node.text.split(delimiter)

                for i in range(len(slices)):
                    if (i+1) % 2 != 0:
                        if  slices[i] == "":
                            continue
                        else:
                            nodes.append(TextNode(slices[i], "text"))
                    else:
                        nodes.append(TextNode(slices[i], text_type))

                new_nodes.extend(nodes)
    return new_nodes