import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }

    def test_htmlnode_to_props(self):
        
        node = HTMLNode(props=self.props)
        html_attributes = node.props_to_html()
        print(html_attributes)
        self.assertEqual(html_attributes, ' href="https://www.google.com" target="_blank"')



if __name__ == "__main__":
    unittest.main()