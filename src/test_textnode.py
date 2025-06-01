import unittest

from textnode import TextNode, TextType

class TesttTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        node3 = TextNode("This is a text node", TextType.LINK_TEXT, "https://www.google.com")
        node4 = TextNode("This is a text node", TextType.LINK_TEXT,"https://www.google.com")
        node5 = TextNode("This is a text node", TextType.CODE_TEXT, None)
        self.assertEqual(node,node2)
        self.assertNotEqual(node,node3)
        self.assertNotEqual(node5,node2)
        self.assertEqual(node4,node3)

if __name__ == "main":
    unittest.main()