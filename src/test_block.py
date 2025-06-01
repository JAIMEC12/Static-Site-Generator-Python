from block import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node
import unittest

class TestBlocks(unittest.TestCase):
    def test(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        self.assertEqual(block_to_block_type("1. Hello\n2. Hola\n3. Hola"), BlockType.ORDERED_LIST)

        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        # print(f"Hola: {html}")
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

        md = """
1. Hola
2. text in a p
3. tag here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(f"Hola: {html}")
        self.assertEqual(
        html,
        "<div><ol><li>Hola</li><li>text in a p</li><li>tag here</li></ol></div>",
    )
        
        md = """
- Hola
- text in a p
- tag here
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(f"Hola: {html}")
        self.assertEqual(
        html,
        "<div><ul><li>Hola</li><li>text in a p</li><li>tag here</li></ul></div>",
    )
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        print(html)
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
