import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node, split_nodes_delimiter
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):
    
    def test_to_html_props(self):
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

    def test_repr(self):
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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")
    
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
    def test_parent_with_empty_children_list(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_multiple_children(self):
        child1 = LeafNode("span", "first")
        child2 = LeafNode("span", "second")
        child3 = LeafNode("span", "third")
        parent_node = ParentNode("div", [child1, child2, child3])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><span>second</span><span>third</span></div>"
        )

    def test_deep_nesting(self):
        leaf1 = LeafNode("b", "bold")
        leaf2 = LeafNode("i", "italic")
        mid_parent1 = ParentNode("p", [leaf1, leaf2])
        leaf3 = LeafNode("a", "link")
        mid_parent2 = ParentNode("div", [leaf3])
        root = ParentNode("section", [mid_parent1, mid_parent2])
        self.assertEqual(
            root.to_html(),
            "<section><p><b>bold</b><i>italic</i></p><div><a>link</a></div></section>"
        )

    def test_with_properties(self):
        child = LeafNode("a", "click me", {"href": "https://boot.dev"})
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            parent.to_html(),
            '<div class="container"><a href="https://boot.dev">click me</a></div>'
        )
    def test_missing_tag_raises_error(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("span", "child")]).to_html()
        self.assertTrue("invalid HTML: no tag" in str(context.exception))

    def test_missing_children_raises_error(self):
        
        parent = ParentNode("div", [LeafNode("span", "child")])
        parent.children = None
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertTrue("invalid HTML: no children" in str(context.exception))

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")

    def test_code(self):
        node = TextNode("This is code", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code")

    def test_link(self):
        node = TextNode("Click me", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props["href"], "https://www.example.com")

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Empty string for image value
        self.assertEqual(html_node.props["src"], "image.png")
        self.assertEqual(html_node.props["alt"], "Alt text")
    
    def test_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        
        assert split_nodes_delimiter([node], "`", TextType.CODE) == [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
    
            ]


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_simple_split(self):
        # Test a simple case with one delimiter pair
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multiple_splits(self):
        # Test with multiple delimiter pairs
        node = TextNode("Text with `code` and another `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, "")

    def test_no_delimiter(self):
        # Test when there's no delimiter in the text
        node = TextNode("Plain text without delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Plain text without delimiters")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_non_text_node(self):
        # Test when the node is not a TEXT type
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Already bold")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_missing_closing_delimiter(self):
        # Test when there's no closing delimiter
        node = TextNode("Text with `code but no closing", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multiple_nodes(self):
        # Test with multiple input nodes
        nodes = [
            TextNode("Text with `code`", TextType.TEXT),
            TextNode("Plain text", TextType.TEXT),
            TextNode("More `code blocks`", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 7)
        # Check node 0: "Text with "
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        # Check node 1: "code"
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        # Check node 2: ""
        self.assertEqual(new_nodes[2].text, "")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        # Check node 3: "Plain text"
        self.assertEqual(new_nodes[3].text, "Plain text")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        # Check node 4: "More "
        self.assertEqual(new_nodes[4].text, "More ")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        # Check node 5: "code blocks"
        self.assertEqual(new_nodes[5].text, "code blocks")
        self.assertEqual(new_nodes[5].text_type, TextType.CODE)
        # Check node 6: ""
        self.assertEqual(new_nodes[6].text, "")
        self.assertEqual(new_nodes[6].text_type, TextType.TEXT)
        
if __name__ == "__main__":
    unittest.main()