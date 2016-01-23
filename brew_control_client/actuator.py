import logging

from interlock import InterlockError


class Actuator(object):

    def __init__(self, issue_command_fun, command_factory, interlocks, logger=None):
        self._issue_command_fun = issue_command_fun
        self._command_factory = command_factory
        self._interlocks = interlocks
        self._logger = logging.getLogger('Actuator') if logger is None else logger

    def _issue_command(self, command):
        self._logger.info("Issue command: {}".format(repr(command)))
        self._issue_command_fun(command.render_as_request_parameters())

    def actuate(self, brew_state):
        if self._may_actuate(brew_state):
            self._actuate(brew_state)
        else:
            self._handle_actuate_interlock_failure(brew_state)

    def deactuate(self, brew_state):
        if self._may_deactuate(brew_state):
            self._deactuate(brew_state)
        else:
            self._handle_deactuate_interlock_failure(brew_state)

    def _may_actuate(self, brew_state):
        return all(i.may_actuate(brew_state) for i in self._interlocks)

    def _may_deactuate(self, brew_state):
        return all(i.may_dectuate(brew_state) for i in self._interlocks)

    def _handle_actuate_interlock_failure(self, brew_state):
        raise InterlockError("Interlock criteria for actuation not met by state: {}".format(brew_state))

    def _handle_deactuate_interlock_failure(self, brew_state):
        raise InterlockError("Interlock criteria for deactuation not met by state: {}".format(brew_state))

    def _actuate(self, brew_state):
        raise NotImplementedError()

    def _deactuate(self, brew_state):
        raise NotImplementedError()


class HeaterActuator(Actuator):
    def _handle_actuate_interlock_failure(self, brew_state):
        self.deactuate(brew_state)


class HEXActuator(HeaterActuator):

    def _actuate(self, brew_state):
        c = self._command_factory.get_hex_on_command()
        self._issue_command(c)

    def _deactuate(self, brew_state):
        c = self._command_factory.get_hex_off_command()
        self._issue_command(c)


class HLTActuator(HeaterActuator):

    def _actuate(self, brew_state):
        c = self._command_factory.get_hlt_on_command()
        self._issue_command(c)

    def _deactuate(self, brew_state):
        c = self._command_factory.get_hlt_off_command()
        self._issue_command(c)

