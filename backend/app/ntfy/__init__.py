import requests
from string import ascii_letters
from random import shuffle, randint

class NtfyMessage(object):
    def __init__(self) -> None:
        self.message = ""
        self.title = ""
        self.attach = ""
        self.tags = ""
        self.action = ""

    
def generate_name(min_length = 5, max_length = 10):
    return shuffle(ascii_letters)[:randint(min_length, max_length)]

def send_message(ntfy_message: NtfyMessage, base_url = "https://ntfy.sh"):
    pass