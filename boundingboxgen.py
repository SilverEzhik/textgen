import atexit
import random
import base64
import os.path
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

charset = \
    """!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~€"""

folder = "data/"


def word():
    s = ""
    l = random.randint(1, 20)

    for _ in range(l):
        s += random.choice(charset)

    if random.random() < 0.1:
        s += random.choice(".,;:!?")

    return s


style = """
body {{
    margin-left: {:d}px;
    margin-right: {:d}px;
    margin-top: {:d}px;
    font-size: {:.2f}em;
}}
"""


def generate_style():
    return style.format(random.randint(0, 25), random.randint(0, 25), random.randint(0, 25), random.uniform(0.7, 1.5))


class Generator:
    template = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1"><style>{style}</style></head><body>{text}</body></html>"""

    id = 0

    def __init__(self, silent=True):
        browser_options = Options()
        browser_options.headless = silent
        self.browser = webdriver.Firefox(options=browser_options)
        self.browser.set_window_size(640, 480 + 74)
        atexit.register(self.browser.close)  # browser killer

    def load(self, html_content):
        self.browser.get(
            "data:text/html;charset=utf-8;base64,{html_content}".format(html_content=base64.standard_b64encode(html_content.encode()).decode()))

    def generate(self):
        l = random.randint(10, 80)
        s = ""
        for _ in range(l):
            s += "<word>{}</word> ".format(word())
        self.load(Generator.template.format(style=generate_style(), text=s))

    def dimensions(self):
        words = g.browser.find_elements_by_tag_name("word")
        return [(round(x.rect["x"], 2), round(x.rect["y"], 2), round(x.rect["width"], 2), round(x.rect["height"], 2)) for x in words]

    def write(self):
        filename = "{0:010d}".format(self.id)
        while os.path.isfile(folder + filename + ".txt"):
            self.id += 1
            filename = "{0:010d}".format(self.id)

        # metrics
        text_file = open(folder + filename + ".txt", "w")
        text_file.write(str(self.dimensions()))

        # screenshot
        self.browser.save_screenshot(folder + filename + ".png")

        # close
        text_file.close()

    def do(self):
        g.generate()
        g.write()


g = Generator()

# while True:
#     g.generate()
#     sleep(5)
