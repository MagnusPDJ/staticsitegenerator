import unittest

from htmlnode import HTMLNode


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
        node = HTMLNode("p","this is a test",None,{
        "href": "https://www.google.com", 
        "target": "_blank",
        }   
        )
        test = 'href="https://www.google.com"target="_blank"'
        self.assertNotEqual(node.props_to_html(), test)

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

if __name__ == "__main__":
    unittest.main()