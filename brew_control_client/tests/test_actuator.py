import unittest
from unittest import TestCase

import mock

from actuator import HEXActuator, HLTActuator
from brew_state import BrewState
from interlock import Interlock
from pin_command import CommandFactory
from pin_config import PinConfig


class BaseHeaterActuatorTestCase(TestCase):
    def setUp(self):
        self._issue_command = mock.Mock()
        self._pin_config = PinConfig()
        self._command_factory = CommandFactory(self._pin_config)
        self._interlock = mock.Mock(spec_set=Interlock)
        self._other_interlock = mock.Mock(spec_set=Interlock)
        self._interlocks = [self._interlock, self._other_interlock]
        self._actuator = self.get_actuator_constructor()(self._issue_command, self._command_factory, self._interlocks)

        self._brew_state = BrewState(
                1.0,
                2.0,
                3.0,
                4.0,
                False,
                True
        )

    def _assert_command_issued(self, c):
        self._issue_command.assert_called_once_with(c.render_as_request_parameters())

    def _check_actuate_with_interlocks_ok(self):
        for lock in self._interlocks:
            lock.may_actuate.return_value = True

        self._actuator.actuate(self._brew_state)
        for lock in self._interlocks:
            lock.may_actuate.assert_called_once_with(self._brew_state)
            self.assertFalse(lock.may_deactuate.called)

        c = self._get_exp_on_command()
        self._assert_command_issued(c)

    def _check_actuate_with_interlocks_faulted(self):
        for lock in self._interlocks:
            lock.may_actuate.return_value = False
            lock.may_deactuate.return_value = True

        self._actuator.actuate(self._brew_state)
        for lock in self._interlocks:
            lock.may_actuate.assert_called_once_with(self._brew_state)
            lock.may_deactuate.assert_called_once_with(self._brew_state)

        c = self._get_exp_off_command()
        self._assert_command_issued(c)

    def _check_deactuate_with_interlocks_faulted(self):
        for lock in self._interlocks:
            lock.may_actuate.return_value = False
            lock.may_deactuate.return_value = True

        self._actuator.deactuate(self._brew_state)
        for lock in self._interlocks:
            self.assertFalse(lock.may_actuate.called)
            lock.may_deactuate.assert_called_once_with(self._brew_state)

        c = self._get_exp_off_command()
        self._assert_command_issued(c)

    def get_actuator_constructor(self):
        raise NotImplementedError()

    def _get_exp_on_command(self):
        raise NotImplementedError()

    def _get_exp_off_command(self):
        raise NotImplementedError()


class TestHEXActuator(BaseHeaterActuatorTestCase):

    def test_actuate_with_interlocks_ok(self):
        self._check_actuate_with_interlocks_ok()

    def test_actuate_with_interlocks_faulted(self):
        self._check_actuate_with_interlocks_faulted()

    def test_deactuate_with_interlocks_faulted(self):
        self._check_deactuate_with_interlocks_faulted()

    def get_actuator_constructor(self):
        return HEXActuator

    def _get_exp_on_command(self):
        return self._command_factory.get_hex_on_command()

    def _get_exp_off_command(self):
        return self._command_factory.get_hex_off_command()

class TestHLTActuator(BaseHeaterActuatorTestCase):

    def test_actuate_with_interlocks_ok(self):
        self._check_actuate_with_interlocks_ok()

    def test_actuate_with_interlocks_faulted(self):
        self._check_actuate_with_interlocks_faulted()

    def test_deactuate_with_interlocks_faulted(self):
        self._check_deactuate_with_interlocks_faulted()

    def get_actuator_constructor(self):
        return HLTActuator

    def _get_exp_on_command(self):
        return self._command_factory.get_hlt_on_command()

    def _get_exp_off_command(self):
        return self._command_factory.get_hlt_off_command()