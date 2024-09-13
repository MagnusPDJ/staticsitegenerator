import unittest

from htmlnode import ParentNode

from textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
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
    
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )
    
    def test_extract_empty(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            []
        )

    def test_textnode_images(self):
        text = [TextNode(
            "This a text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) as a funny meme.",
            "text"
        )]
        self.assertEqual(
            str(split_nodes_image(text)),
            "[TextNode(This a text with a , text, None), TextNode(rick roll, image, https://i.imgur.com/aKaOqIh.gif), TextNode( and , text, None), TextNode(obi wan, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( as a funny meme., text, None)]"
        )

    def test_textnode_links(self):
        text = [TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            "text"
        )]
        self.assertEqual(
            str(split_nodes_link(text)),
            "[TextNode(This is text with a link , text, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( and , text, None), TextNode(to youtube, link, https://www.youtube.com/@bootdotdev)]"
        )

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertEqual(
            str(textnodes),
            "[TextNode(This is , text, None), TextNode(text, bold, None), TextNode( with an , text, None), TextNode(italic, italic, None), TextNode( word and a , text, None), TextNode(code block, code, None), TextNode( and an , text, None), TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( and a , text, None), TextNode(link, link, https://boot.dev)]"
        )


    def test_block_split(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.





* This is the first list item in a list block
* This is a list item
* This is another list item"""
        list = markdown_to_blocks(markdown)
        self.assertEqual(
            str(list),
            "['# This is a heading', 'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', '* This is the first list item in a list block\\n* This is a list item\\n* This is another list item']"
        )

    def test_block_type(self):
        block = "###### This is a heading 6"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )
    def test_block_type1(self):
        block = "##### This is a heading 5"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )
    def test_block_type2(self):
        block = "#### This is a heading 4"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )
    def test_block_type3(self):
        block = "### This is a heading 3"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )
    def test_block_type4(self):
        block = "## This is a heading 2"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )
    def test_block_type5(self):
        block = "# This is a heading 1"
        self.assertEqual(
            block_to_block_type(block),
            "heading"
        )
    def test_block_type6(self):
        block = "```\nThis is a code block\n```"
        self.assertEqual(
            block_to_block_type(block),
            "code"
        )
    def test_block_type7(self):
        block = ">this is a quote\n>this is also a quote\n>this is definitely a quote"
        self.assertEqual(
            block_to_block_type(block),
            "quote"
        )
    def test_block_type8(self):
        block = "* this is a list\n* this is also an item\n* more items"
        self.assertEqual(
            block_to_block_type(block),
            "unordered_list"
        )
    def test_block_type9(self):
        block = "- item\n- another\n- lol"
        self.assertEqual(
            block_to_block_type(block),
            "unordered_list"
        )
    def test_block_type10(self):
        block = "1. this\n2. is\n3. an ordered list"
        self.assertEqual(
            block_to_block_type(block),
            "ordered_list"
        )

if __name__ == "__main__":
    unittest.main()