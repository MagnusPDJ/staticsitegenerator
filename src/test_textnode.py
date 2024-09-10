import unittest

from textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    
    def test1(self):
        node = TextNode("This is a text", "bold")
        node2 = TextNode("This is a text", "italic")
        self.assertNotEqual(node, node2)

    def test2(self):
        node = TextNode("This is a text", "bold")
        node2 = TextNode("This is not a text", "bold")
        self.assertNotEqual(node, node2)

    def test3(self):
        node = TextNode("This is a text", "bold", "http://www.boot.dev")
        node2 = TextNode("This is a text", "bold")
        self.assertNotEqual(node, node2)       

    def test_convert(self):
        textnode = TextNode("This is my text", TextType.text_type_bold.value)
        self.assertEqual(
            text_node_to_html_node(textnode).__repr__(),
            "LeafNode(b, This is my text, None)"
        )

    def test_convert1(self):
        textnode = TextNode("This is my text", TextType.text_type_text.value)
        self.assertEqual(
            text_node_to_html_node(textnode).__repr__(),
            "LeafNode(None, This is my text, None)"
        )

    def test_convert2(self):
        textnode = TextNode("This is my text", TextType.text_type_bold.value)
        self.assertEqual(
            text_node_to_html_node(textnode).to_html(),
            "<b>This is my text</b>"
        )
    
    def test_convert3(self):
        textnode = TextNode("This is an image", TextType.text_type_image.value, "url/of/image.jpg")
        self.assertEqual(
            text_node_to_html_node(textnode).__repr__(),
            "LeafNode(img, , {'src': 'url/of/image.jpg', 'alt': 'This is an image'})"
        )
        self.assertEqual(
            text_node_to_html_node(textnode).to_html(),
            '<img src="url/of/image.jpg" alt="This is an image">'
        )

if __name__ == "__main__":
    unittest.main()