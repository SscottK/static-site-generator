from textnode import TextNode, TextType
import re

class HTMLNode():
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:            
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        self.props = props
    
    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value
        
        
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, props)
        
        self.children = children
        self.props = props
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        childs = ""
        for child in self.children:
            
            childs += child.to_html()
        result = f"<{self.tag}{self.props_to_html()}>{childs}</{self.tag}>"
        
        return result
    

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid TextType: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    

    new_nodes = []
    
    for old_node in old_nodes:
        # If not a TEXT node, keep as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
            
        # Process TEXT nodes to find delimiters
        text = old_node.text
        result = []
        
        # Continue searching until no more delimiters
        while delimiter in text:
            # Find opening delimiter
            start_index = text.find(delimiter)
            if start_index == -1:
                break
                
            # Find closing delimiter
            end_index = text.find(delimiter, start_index + len(delimiter))
            if end_index == -1:
                raise ValueError(f"Closing delimiter not found: {delimiter}")
                
            # Extract parts
            before_text = text[:start_index]
            delimited_text = text[start_index + len(delimiter):end_index]
            
            # Add before_text if not empty
            if before_text:
                result.append(TextNode(before_text, TextType.TEXT))
                
            # Add delimited text with specified type
            result.append(TextNode(delimited_text, text_type))
            
            # Update text to remaining portion
            text = text[end_index + len(delimiter):]
         
        # Add any remaining text
        
        result.append(TextNode(text, TextType.TEXT))
            
        # Add all newly created nodes to the result
        new_nodes.extend(result)
            
    return new_nodes


def extract_markdown_images(text):
    """
    Extracts markdown images from text and returns a list of tuples.
    Each tuple contains the alt text and the URL of the image.

    Args:
        text: The markdown text to extract images from.

    Returns:
        A list of tuples, where each tuple contains the alt text and URL of an image.
    """
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(image_pattern, text)
    return matches


def extract_markdown_links(text):
    """
    Extracts markdown links from text and returns a list of tuples.
    Each tuple contains the anchor text and the URL of the link.

    Args:
        text: The markdown text to extract links from.

    Returns:
        A list of tuples, where each tuple contains the anchor text and URL of a link.
    """
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(link_pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # If not a TEXT node, keep as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Check if there are any images to extract
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
            continue
        
        # Process the text with images
        text = old_node.text
        current_index = 0
        
        # For each image found
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            image_index = text.find(image_markdown, current_index)
            
            # Add text before the image if any
            if image_index > current_index:
                new_nodes.append(
                    TextNode(text[current_index:image_index], TextType.TEXT)
                )
            
            # Add the image node
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Move past this image
            current_index = image_index + len(image_markdown)
        
        # Add remaining text only if not empty
        remaining_text = text[current_index:]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    
    for old_node in old_nodes:
        # If not a TEXT node, keep as is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Check if there are any links to extract
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
            continue
        
        # Process the text with links
        text = old_node.text
        current_index = 0
        
        # For each link found
        for link_text, url in links:
            link_markdown = f"[{link_text}]({url})"
            link_index = text.find(link_markdown, current_index)
            
            # Add text before the link if any
            if link_index > current_index:
                new_nodes.append(
                    TextNode(text[current_index:link_index], TextType.TEXT)
                )
            
            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            # Move past this link
            current_index = link_index + len(link_markdown)
        
        # Add remaining text only if not empty
        remaining_text = text[current_index:]
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes