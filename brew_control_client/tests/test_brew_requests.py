import unittest

from brew_control_client.brew_requests import get_index_response


from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class TestIndexRequest(unittest.TestCase):

    def test_get_index_response(self):
        response = get_index_response()
        pass