import requests
import json

from brew_control_client.ml_stripper import strip_tags

brew_host = '192.168.11.101'
host_url_head = 'http://'+brew_host+'/'
state_url = 'state.json'
reserved_url = 'reserved.json'
pincommand_url = 'pincommand'

def get_index_response():
    return requests.get(host_url_head)

def get_state_response():
    return requests.get('/'.join([host_url_head, state_url]))

def get_reserved_response():
    return requests.get('/'.join([host_url_head, reserved_url]))

def get_pincommand_response(commands):
    """
     commands = {'key1': 'value1', 'key2': ['value2', 'value3']}
     becomes
     ?key1=value1&key2=value2&key2=value3
     """
    return requests.get('/'.join([host_url_head, pincommand_url]), params=commands)

def get_index_str():
    return strip_tags(get_index_response().text)

def get_state():
    return get_state_response().json()

def get_reserved_pins():
    return get_reserved_response().json()['reserved']

def get_interrupt_pins():
    return get_reserved_response().json()['interrupt']