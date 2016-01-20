import unittest

from brew_control_client.brew_requests import get_index_response




class TestIndexRequest(unittest.TestCase):

    def test_get_index_response(self):
        response = get_index_response()
        pass