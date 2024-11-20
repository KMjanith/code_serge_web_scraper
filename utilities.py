import re


class Utilities:
    def __init__(self):
        pass

    #function to remove ascii characters from the string
    def remove_ascii(self,text):
        return re.sub(r'[^\x00-\x7F]+', '', text)