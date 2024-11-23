import json
import requests
from constants import React
from bs4 import BeautifulSoup
import re

class ReactFunction:

    def __init__(self):
        pass

    #function to find the main topics and their subtopics with the urls
    def find_outer_topis(self,soup, url):
        aside = soup.find(React.ASIDE.value)
        nav = aside.find(React.NAV.value)
        all_li = nav.find_all(React.LI.value)
        outer_li = [li for li in all_li if li.find(React.UL.value)]

        #dictionary to store the toic hirachy
        result = {}
        for i in outer_li:
            main_sub_topic = i.find(React.A.value).find(React.DIV.value).text   #main sub topics in aside nav bar
            result[main_sub_topic] = {}
            inner_li = i.find(React.UL.value).find_all(React.LI.value)

            # getting sub topics and their urls for the main sub topics
            for j in inner_li:
                subtopic_url = url + j.find(React.A.value).get(React.HREF.value)
                result[main_sub_topic][j.find(React.A.value).text] ={"url": subtopic_url}
        return result

    #function to get the inner content of the urls
    def getting_inner_content(self,url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all headers in order
        headers = soup.find("main").find("article").find_all(React.TOPIC_LIST.value)

        # structure to hold the hierarchical content
        content = []
        stack = [{"level": 0, "content": content}]

        for header in headers:
            tag_level = int(header.name[1])  # Extract level from 'h1', 'h2', etc.
            header_content = {
                "header": header.text.strip(),
                "content": [],
            }

            # Collect all text until the next header of the same or higher level
            siblings = []
            code_snippets = []
            for sibling in header.find_next_siblings():

                if sibling.name in React.TOPIC_LIST.value and int(sibling.name[1]) <= tag_level:
                    break  # Stop at the next header of the same or higher level
                if sibling.name == 'div' or sibling.name == 'code' :  # Detect <code> tags
                    code_snippets.append(sibling.get_text(strip=True)) 
                elif sibling.name and sibling.get_text(strip=True):  # Only include non-empty text
                    text = sibling.get_text(strip=True)
                    cleaned_text = text.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
                    siblings.append(cleaned_text)
                    

            # Add the collected text content
            header_content["content"] = siblings
            if code_snippets:
                header_content["code_examples"] = code_snippets  # Add code snippets as a separate key

            # Find the right place to insert this header based on its level
            while stack and stack[-1]["level"] >= tag_level:
                stack.pop()

            stack[-1]["content"].append(header_content)
            stack.append({"level": tag_level, "content": header_content["content"]})

        return json.dumps(content, indent=4)

    #function to extract the urls from the json content
    def extract_links_from_json(self,json_content):
        links = []
        for key, value in json_content.items():
            links.append(value["url"])
            for sub_key, sub_value in value.items():
                links.append(sub_value["url"])
        return links

    def get_cotent_data(self,link_list):
        body_content = []
        link_list = link_list[:1]
        for link in link_list:
            json_content = self.getting_inner_content(link)
            body_content.append(json_content)
            print(json_content)
        # open('react.json', 'w').write(json.dumps(body_content, indent=4))   
   
        return body_content 
    





