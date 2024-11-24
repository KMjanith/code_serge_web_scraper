import json
import requests
from aws.aws_constants import Aws
from react.react_constants import React
from bs4 import BeautifulSoup
import re

class AwsFunction:

    def __init__(self):
        pass

    def make_url_hirachy(self, topic_list):
        for i in topic_list:
            if(i.get(Aws.CONTENTS.value)):
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                i[Aws.SECTIONS.value] = []
                self.make_url_hirachy(i[Aws.CONTENTS.value])
            else:
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                i[Aws.SECTIONS.value] = []


    #function to find the main topics and their subtopics with the urls
    def find_outer_topis(self):
        res = requests.get(Aws.TOPIC_URL.value)
        contents = []
        # Extract the URLs of the sections
        for i in res.json()[Aws.CONTENTS.value]:
            if i[Aws.TITLE.value] in Aws.MAIN_TOPICS.value:
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                contents.append(i)
    
        return contents