from fake_server import FakeServer
from pin_config import INTERRUPT_PINS, RESERVED_PINS, PinConfig
from tests.test_brew_server import BrewServerTest


class FakeServerTest(BrewServerTest):
    def setUp(self):
        self._server = FakeServer(RESERVED_PINS, INTERRUPT_PINS)
        self._pin_nr = PinConfig().HLT_actuation_pin
        self._server.set_pinmode(self._pin_nr, FakeServer.PINMODE_OUT)
