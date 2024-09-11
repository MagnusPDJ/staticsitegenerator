import unittest

from htmlnode import ParentNode

from textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node,
    split_nodes_delimiter
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
    
    def test_splitting0(self):
        nodes = [TextNode("This *is a test to see if my code works.", "text")]
        with self.assertRaises(Exception):
            new_nodes = split_nodes_delimiter(nodes, "*", "italic")

    def test_splitting(self):
        nodes = [TextNode("This *is* a **test to see** if my `code` works.", "text")]
        new_nodes = split_nodes_delimiter(nodes, "**", "bold")
        new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
        new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This , text, None), TextNode(is, italic, None), TextNode( a , text, None), TextNode(test to see, bold, None), TextNode( if my , text, None), TextNode(code, code, None), TextNode( works., text, None)]"
        )

    def test_splitting1(self):
        nodes = [TextNode("This **is** a *test to see* if my `code` works.", "text")]
        new_nodes = split_nodes_delimiter(nodes, "*", "italic")
        new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
        new_nodes = split_nodes_delimiter(new_nodes, "**", "bold")
        self.assertNotEqual(
            str(new_nodes),
            "[TextNode(This , text, None), TextNode(is, bold, None), TextNode( a , text, None), TextNode(test to see, italic, None), TextNode( if my , text, None), TextNode(code, code, None), TextNode( works., text, None)]"
        )

    def test_splitting2(self):
        nodes = [TextNode("This *is* a test to see if my *code works*.", "text")]
        new_nodes = split_nodes_delimiter(nodes, "*", "italic")
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This , text, None), TextNode(is, italic, None), TextNode( a test to see if my , text, None), TextNode(code works, italic, None), TextNode(., text, None)]"
        )

    def test_splitting3(self):
        nodes = [TextNode("`This is` a test to see if my code `works.`", "text")]
        new_nodes = split_nodes_delimiter(nodes, "`", "code")
        print(new_nodes)
        self.assertEqual(
            str(new_nodes),
            "[TextNode(This is, code, None), TextNode( a test to see if my code , text, None), TextNode(works., code, None)]"
        )

    
    def test_splitting_to_html(self):
        nodes = [TextNode("This **is** a *test to see* if my `code` works.", "text")]
        new_nodes = split_nodes_delimiter(nodes, "**", "bold")
        new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
        new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
        html_nodes = []
        for node in new_nodes:
            html_nodes.append(text_node_to_html_node(node))
        parent = ParentNode("p", html_nodes)
        self.assertEqual(
            parent.to_html(),
            "<p>This <b>is</b> a <i>test to see</i> if my <code>code</code> works.</p>"
        )

if __name__ == "__main__":
    unittest.main()