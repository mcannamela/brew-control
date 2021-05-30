import unittest

from brew_control_client.brew_server import BrewServer
from brew_control_client.brew_state import RawState
from brew_control_client.pin_command import CommandWords
from brew_control_client.pin_config import PinConfig


class BrewServerTest(unittest.TestCase):

    def setUp(self):
        self._server = BrewServer()
        self._pin_nr = PinConfig().HLT_actuation_pin

    def test_get_raw_state(self):
        s = self._server.get_raw_state()
        self.assertTrue(isinstance(s, RawState))

    def test_issue_pin_commands(self, commands=None):
        command_words = [
            CommandWords.SET_PINMODE_OUT,
            CommandWords.SET_PIN_HIGH,
            CommandWords.SET_PIN_LOW,
            CommandWords.SET_PINMODE_IN
        ]
        for c in command_words:
            self._server.issue_pin_commands({c: [self._pin_nr]})

    def test_get_index_str(self):
        self.assertTrue(isinstance(self._server.get_index_str(), str))

    def test_get_reserved_pins(self):
        self.assertTrue(all([isinstance(n, int) for n in self._server.get_reserved_pins()]))

    def test_get_interrupt_pins(self):
        self.assertTrue(all([isinstance(n, int) for n in self._server.get_reserved_pins()]))
