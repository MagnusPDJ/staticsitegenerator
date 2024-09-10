import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()