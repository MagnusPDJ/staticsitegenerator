import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test0(self):
        node = HTMLNode(
            "p",
            "this is a test",
            None,
            None
        )
        self.assertEqual(
            node.props_to_html(),
            ""
        )

    def test1(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test2(self):
        node = HTMLNode(
            "p",
            "this is a test",
            None,
            {"href": "https://www.google.com", "target": "_blank"}   
        )
        self.assertNotEqual(
            node.props_to_html(), 
            'href="https://www.google.com"target="_blank"'
        )

    def test3(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
    
    def test_none(self):
        node = LeafNode(
            None,
            "Hello, world!"
        )
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_paragraph(self):
        node = LeafNode(
            "p",
            "This is a paragraph of text."
        )
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>"
        )

    def test_bold(self):
        node = LeafNode(
            "b",
            "This is a paragraph of text."
        )
        self.assertEqual(
            node.to_html(),
            "<b>This is a paragraph of text.</b>"
        )

    def test_italic(self):
        node = LeafNode(
            "i",
            "This is a paragraph of text."
        )
        self.assertEqual(
            node.to_html(),
            "<i>This is a paragraph of text.</i>"
        )

    def test_code(self):
        node = LeafNode(
            "code",
            "This is a paragraph of text."
        )
        self.assertEqual(
            node.to_html(),
            "<code>This is a paragraph of text.</code>"
        )

    def test_link(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )
    
    def test_block(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
    
    def test_block1(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]

                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]

                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<body><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></body>"
        )

    def test_block2(self):
        node = ParentNode(
            "body",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("a", "Click me!", {"href": "https://www.google.com"})
                    ]
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]

                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<body><p><a href="https://www.google.com">Click me!</a></p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></body>'
        )

    
    
    def test_no_child(self):
        node = ParentNode(
            "p",
            None,
        )
        with self.assertRaises(ValueError):
            node.to_html()
        
if __name__ == "__main__":
    unittest.main()