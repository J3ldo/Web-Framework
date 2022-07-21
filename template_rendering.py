from jinja2 import Environment, PackageLoader, select_autoescape
import os
import shutil

jinja = Environment(
    loader=PackageLoader(__name__),
    autoescape=select_autoescape()
)


def render_template(template, **kwargs):
    if not os.path.exists(__file__[:-21] + 'templates/' + template):
        shutil.copy(template, __file__[:-21] + "/templates")

    return jinja.get_template(template).render(kwargs, get_flashed_messages=get_flashed_messages)


def redirect(location, time=0, content=""):
    return f'''
    <head>
        <meta http-equiv="refresh" content="{time}; URL={location}" />
    </head>
    {content}
    '''


flashed_queue = []

def flash(message: str, category: str):
    global flashed_queue
    flashed_queue.append([message, category])


def get_flashed_messages():
    global flashed_queue
    flashed_queue_old = flashed_queue
    flashed_queue = []
    return flashed_queue_old

def safe_template_string(text):
    out = ""
    text = list(text)
    for idx, item in enumerate(text):
        if item == "{":
            if text[idx+1] == "{":
                out += "​"

        text += item

    return text

