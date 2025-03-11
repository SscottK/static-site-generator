from textnode import TextNode, TextType

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