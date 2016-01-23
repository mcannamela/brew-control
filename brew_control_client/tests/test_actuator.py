import unittest
import mock

from actuator import HEXActuator
from brew_state import BrewState
from interlock import Interlock
from pin_command import CommandFactory
from pin_config import PinConfig


class TestHEXActuator(unittest.TestCase):

    def setUp(self):
        self._issue_command = mock.Mock()
        self._pin_config = PinConfig()
        self._command_factory = CommandFactory(self._pin_config)
        self._interlock = mock.Mock(spec_set=Interlock)
        self._other_interlock = mock.Mock(spec_set=Interlock)
        self._interlocks = [self._interlock, self._other_interlock]
        self._actuator = HEXActuator(self._issue_command, self._command_factory, self._interlocks)

        self._brew_state = BrewState(
                1.0,
                2.0,
                3.0,
                4.0,
                False,
                True
        )

    def test_actuate_with_interlocks_ok(self):
        for lock in self._interlocks:
            lock.may_actuate.return_value = True

        self._actuator.actuate(self._brew_state)
        for lock in self._interlocks:
            lock.may_actuate.assert_called_once_with(self._brew_state)
            self.assertFalse(lock.may_deactuate.called)

        self._issue_command.assert_called_once_with(self._command_factory.get_hex_on_command().render_as_request_parameters())

    def test_actuate_with_interlocks_faulted(self):
        for lock in self._interlocks:
            lock.may_actuate.return_value = False
            lock.may_deactuate.return_value = True

        self._actuator.actuate(self._brew_state)
        for lock in self._interlocks:
            lock.may_actuate.assert_called_once_with(self._brew_state)
            lock.may_deactuate.assert_called_once_with(self._brew_state)

        self._issue_command.assert_called_once_with(self._command_factory.get_hex_off_command().render_as_request_parameters())

    def test_deactuate_with_interlocks_faulted(self):
        for lock in self._interlocks:
            lock.may_actuate.return_value = False
            lock.may_deactuate.return_value = True

        self._actuator.deactuate(self._brew_state)
        for lock in self._interlocks:
            self.assertFalse(lock.may_actuate.called)
            lock.may_deactuate.assert_called_once_with(self._brew_state)

        self._issue_command.assert_called_once_with(self._command_factory.get_hex_off_command().render_as_request_parameters())