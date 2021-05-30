from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self, **kwargs):
        self.reset()
        self.fed = []
        super(MLStripper, self).__init__(**kwargs)

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
