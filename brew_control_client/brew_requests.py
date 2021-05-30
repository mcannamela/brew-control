import requests

from brew_control_client.brew_state import RawState
from brew_control_client.ml_stripper import strip_tags

brew_host = '192.168.11.111'
host_url_head = 'http://'+brew_host
state_url = 'state.json'
reserved_url = 'reserved.json'
pincommand_url = 'pincommand'
timeout_seconds = 5.0


def get_index_response():
    return requests.get(host_url_head, timeout=timeout_seconds)


def get_state_response():
    return requests.get('/'.join([host_url_head, state_url]), timeout=timeout_seconds)


def get_reserved_response():
    return requests.get('/'.join([host_url_head, reserved_url]), timeout=timeout_seconds)


def get_pincommand_response(commands=None):
    """
     commands = {'key1': 'value1', 'key2': ['value2', 'value3']}
     becomes
     ?key1=value1&key2=value2&key2=value3
     """
    commands = {} if commands is None else commands
    return requests.get('/'.join([host_url_head, pincommand_url]), params=commands, timeout=timeout_seconds)


def get_index_str():
    return strip_tags(get_index_response().text)


def get_state():
    return get_state_response().json()


def get_raw_state():
    return RawState(get_state())


def get_reserved_pins():
    return get_reserved_response().json()['reserved']


def get_interrupt_pins():
    return get_reserved_response().json()['interrupt']


class CommandFailed(RuntimeError):
    pass

def issue_commands(commands=None):
    response = get_pincommand_response(commands)
    if not 'retcode 0, OK' in response.text:
        raise CommandFailed(response.text)

