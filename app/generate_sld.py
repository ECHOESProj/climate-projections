from app.init import get_path
from string import Template


def generate_sld(name: str, min: float, max: float, min_color: str, max_color: str):
    with open(get_path('assets/styles/dynamic.sld'), 'r') as f:
        template = Template(f.read())
        output = template.substitute({
            'name':name, 
            'min':str(min), 
            'max':str(max),
            'min_color':min_color,
            'max_color':max_color
        })
    return output


