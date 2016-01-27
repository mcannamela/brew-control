from brew_control_client.brew_requests import get_index_str, get_reserved_pins, get_interrupt_pins, get_raw_state, \
    issue_commands


class BrewServer(object):

    def get_raw_state(self):
        return get_raw_state()

    def issue_pin_commands(self, commands=None):
        issue_commands(commands)

    def get_index_str(self):
        return get_index_str()

    def get_reserved_pins(self):
        return get_reserved_pins()

    def get_interrupt_pins(self):
        return get_interrupt_pins()