import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

def render_template(template_name,context={}):
    template = env.get_template(template_name)
    rendered = template.render(**context)
    return [rendered.encode("utf-8")]
