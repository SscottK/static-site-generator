

class HTMLNode():
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_attributes = " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        return html_attributes
    
    def __repr__(self):
        return f'tag = {self.tag}\n value = {self.value}\n children = {self.children}\n props = {self.props}\n'