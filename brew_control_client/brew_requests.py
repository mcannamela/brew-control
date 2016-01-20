import requests
brew_host = '192.168.11.101'

def get_index_response():
    return requests.get('http://'+brew_host)