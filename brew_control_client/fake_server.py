import sys

from brew_requests import CommandFailed
from brew_state import RawState
from pin_command import CommandWords


class ReservedPinError(ValueError):
    pass

class IllegalWriteToInputPin(ValueError):
    pass

class FakeServer(object):
    PINMODE_IN = 'INPUT'
    PINMODE_OUT = 'OUTPUT'

    def __init__(self, reserved_pins, interrupt_pins):
        self._reserved_pins = reserved_pins
        self._interrupt_pins = interrupt_pins

        self._digital_state = 16*[False]
        self._analog_state = 5*[0.0]
        self._interrupt_frequencies = 2*[0.0]
        self._pinmode = [self.PINMODE_IN for x in self._digital_state]

    def get_raw_state(self):
        return RawState({
            RawState._DIGITAL_KEY: self._digital_state,
            RawState._ANALOG_KEY: self._analog_state,
            RawState._INTERRUPT_KEY: self._interrupt_frequencies
        })

    def issue_pin_commands(self, commands):
        for command_word, pin_nrs in commands.items():
            f = self._get_command_fun(command_word)
            for pin_nr in pin_nrs:
                try:
                    f(pin_nr)
                except ReservedPinError as e:
                    raise CommandFailed, str(e), sys.exc_info()[2]

    def get_index_str(self):
        return "Welcome to FakeBrew!"

    def get_reserved_pins(self):
        return [n for n in self._reserved_pins]

    def get_interrupt_pins(self):
        return [n for n in self._interrupt_pins]

    def set_digital_state(self, pin_nr, state):
        self._digital_state[pin_nr] = bool(state)

    def get_digital_state(self, pin_nr):
        return self._digital_state[pin_nr]

    def set_pinmode(self, pin_nr, mode):
        self._pinmode[pin_nr] = mode

    def set_analog_state(self, pin_nr, state):
        self._analog_state[pin_nr] = float(state)

    def set_interrupt_frequency(self, interrupt_index, state):
        self._interrupt_frequencies[interrupt_index] = float(state)

    def _set_pinmode_out(self, pin_nr):
        self._raise_if_reserved(pin_nr)
        self._pinmode[pin_nr] = self.PINMODE_OUT


    def _set_pinmode_in(self, pin_nr):
        self._raise_if_reserved(pin_nr)
        self._pinmode[pin_nr] = self.PINMODE_IN

    def _set_pin_high(self, pin_nr):
        self._raise_if_reserved(pin_nr)
        self._raise_if_writing_to_input_pin(pin_nr)
        self._digital_state[pin_nr] = True

    def _set_pin_low(self, pin_nr):
        self._raise_if_reserved(pin_nr)
        self._raise_if_writing_to_input_pin(pin_nr)
        self._digital_state[pin_nr] = False

    def _get_command_fun(self, command_word):
        try:
            f = {
                CommandWords.SET_PIN_HIGH: self._set_pin_high,
                CommandWords.SET_PIN_LOW: self._set_pin_low,
                CommandWords.SET_PINMODE_IN: self._set_pinmode_in,
                CommandWords.SET_PINMODE_OUT: self._set_pinmode_out,
            }[command_word]
            return f
        except KeyError:
            raise CommandFailed("{} unknown".format(command_word))

    def _raise_if_writing_to_input_pin(self, pin_nr):
        if self._pinmode[pin_nr] == self.PINMODE_IN:
            raise IllegalWriteToInputPin("{} is in {} mode".format(pin_nr, self.PINMODE_IN))


    def _raise_if_reserved(self, pin_nr):
        if self._is_reserved(pin_nr):
            raise ReservedPinError("{} is reserved".format(pin_nr))



    def _is_reserved(self, pin_nr):
        return pin_nr in self._reserved_pins

