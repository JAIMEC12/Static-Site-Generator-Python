import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    def test(self):
        html_node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        html_node2 = HTMLNode("p","Hello World", props={"href": "https://www.google.com", "target": "_blank"})
        test_html_node = HTMLNode("h1", "Nice to meet you")
        self.assertEqual(html_node.props_to_html(), 'href="https://www.google.com" target="_blank"')
        self.assertNotEqual(html_node.props_to_html(), 'href=https://www.google.com target=_blank' )
        self.assertEqual(test_html_node.props_to_html(), "")
        self.assertNotEqual(html_node2, html_node)
        self.assertEqual(html_node2.children, None)

    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertNotEqual(node.to_html(),"<p> Hello World <p>")
        self.assertEqual(node2.to_html(), "<h1>Hello, world!</h1>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    

    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")