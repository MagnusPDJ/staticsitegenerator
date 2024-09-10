from textnode import TextNode
from htmlnode import LeafNode, ParentNode

def main():
    textnode = TextNode("This is a text node", "bold", "https://www.boot.dev")   
    print(textnode)

main()