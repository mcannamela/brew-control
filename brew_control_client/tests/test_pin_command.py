import unittest

from pin_command import OnCommand, OffCommand, SetupOutputCommand, SetupInputCommand


class TestPinCommands(unittest.TestCase):
    def setUp(self):
        self._pin_nr = 3

    def test_on_command(self):
        self._check_command(OnCommand)

    def test_off_command(self):
        self._check_command(OffCommand)

    def test_ouput_command(self):
        self._check_command(SetupOutputCommand)

    def test_input_command(self):
        self._check_command(SetupInputCommand)

    def _check_command(self, constructor):
        c = constructor(self._pin_nr)
        r = c.render_as_request_parameters()
        self.assertEqual(1, len(r))
        self.assertTrue(isinstance(r.keys()[0], basestring))
        self.assertEqual(r.values()[0], [self._pin_nr])