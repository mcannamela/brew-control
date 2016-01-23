from pin_config import PinConfig


class PinCommand(object):

    def render_as_request_parameters(self):
        raise NotImplementedError()


class SinglePinCommand(PinCommand):

    def __init__(self, pin_number):
        self._pin_number = pin_number

    def __repr__(self):
        return "<{}: {}={}>".format(self.__class__.__name__, self._get_command_word(), self._get_pin_number())

    def render_as_request_parameters(self):
        return {self._get_command_word(): [self._get_pin_number()]}

    def _get_command_word(self):
        raise NotImplementedError()

    def _get_pin_number(self):
        return self._pin_number


class OnCommand(SinglePinCommand):

    def _get_command_word(self):
        return 'SET_PIN_HIGH'


class OffCommand(SinglePinCommand):

    def _get_command_word(self):
        return 'SET_PIN_LOW'


class SetupOutputCommand(SinglePinCommand):
    def _get_command_word(self):
        return 'SET_PINMODE_OUTPUT'


class SetupInputCommand(SinglePinCommand):
    def _get_command_word(self):
        return 'SET_PINMODE_INPUT'


class CompoundPinCommand(PinCommand):

    def __init__(self, pin_commands):
        self._commands = pin_commands

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, ', '.join(map(repr, self._commands)))

    def render_as_request_parameters(self):
        p = {}
        for c in self._commands:
            this_p = c.render_as_request_parameters
            for k, v in this_p:
                if k in p:
                    p[k].extend(v)
                else:
                    p[k] = [].extend(v)


class CommandFactory(object):

    def __init__(self, pin_config):
        self._pin_config = pin_config
        assert isinstance(self._pin_config, PinConfig)

    def get_setup_command(self):
        hex_command = SetupOutputCommand(self._pin_config.HEX_actuator_pin)
        hlt_command = SetupOutputCommand(self._pin_config.HLT_actuator_pin)
        return CompoundPinCommand([hex_command, hlt_command])

    def get_hex_on_command(self):
        return OnCommand(self._pin_config.HEX_actuator_pin)

    def get_hlt_on_command(self):
        return OnCommand(self._pin_config.HLT_actuator_pin)

    def get_hex_off_command(self):
        return OffCommand(self._pin_config.HEX_actuator_pin)

    def get_hlt_off_command(self):
        return OffCommand(self._pin_config.HLT_actuator_pin)



