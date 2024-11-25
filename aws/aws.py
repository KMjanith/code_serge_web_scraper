import json
import requests
from constants.aws_constants import Aws
from constants.react_constants import React
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright

from utilities.utilities import Utilities

class AwsFunction:

    def __init__(self):
        pass

    # function to modify the urls to make them complete
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
                i[Aws.SECTIONS.value] = []
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                contents.append(i)
    
        return contents
    
    
    def data_organizer(self,l, main_header, url):
        stack = [{"headers":main_header, "url": url,"content": []}]  
        original = []
        for i in l:
            if(i.name == None):
                continue
            if(i.name in ['h1', 'h2', 'h3', 'h4']):
                level = int(i.name[1])
                current_stack_length = len(stack)
                if(current_stack_length < level):
                    stack.append({"sub_header": i.text, "content": []})
                elif(current_stack_length == level and current_stack_length != 0):
                    a = stack.pop()
                    stack[-1]["content"].append(a)
                    stack.append({"sub_header": i.text, "content": []})
                
                else:
                    while(len(stack) > level):
                        a = stack.pop()
                        stack[-1]["content"].append(a)
                    a = stack.pop()
                    if(len(stack)==0):
                        original.append(a)
                        stack.append({"sub_header": i.text, "content": []})
                    else:
                        stack[-1]["content"].append(a)
                        stack.append({"sub_header": i.text, "content": []})
            else:
                if(i.name == 'ul'):
                    for index,j in enumerate(i.find_all('li')):
                        stack[-1]["content"].append(f"  {index+1}.{j.text}")
                if(i.name == 'ol'):
                    for index,j in enumerate(i.find_all('li')):
                        stack[-1]["content"].append(f"  {index+1}.{j.text}")

                if(i.name == 'div'):
                    code = i.find('code')

                    if(code):
                        stack[-1]["content"].append({"code_example": code.text})

                    elif(i.find('dl')):
                        dl = i.find('dl')
                        dt = dl.find_all('dt')
                        dd = dl.find_all('dd')
                        for index, j in enumerate(dt):
                            stack[-1]["content"].append(f"  {index+1}.{dt[index].text} : {dd[index].text}")


                    elif(i.find('ul')):
                        for index,j in enumerate(i.find_all('li')):
                            try:
                                header =  j.find('p').find("b").text
                                stack[-1]["content"].append(f"  {index+1}.{header} {j.find('p').text.replace(header, '')}")
                            except: AttributeError
                        
                    else:
                        stack[-1]["content"].append(i.text)
            
                else:
                    if(i.name == "ul" or i.name == "ol" or i.text == ""):
                        continue
                    else:
                        stack[-1]["content"].append(i.text.replace("\n", ""))

        util = Utilities()
        return util.return_data(stack, "content")
    
    #function to get the html content of the urls
    def getting_inner_content(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url)

            # Wait for the AJAX content to load (e.g., by waiting for a specific element)
            page.wait_for_selector('main', timeout=60000)  # Wait for dynamic content for up to 60 seconds

            title_element = page.query_selector('div#main')
            inner_html_content = title_element.inner_html() if title_element else ""
            
            # Parse HTML and filter specific tags using BeautifulSoup
            soup = BeautifulSoup(inner_html_content, "html.parser")

            main_col_body = soup.find('div', id="main-col-body") 
            mainbody_content = main_col_body.contents

            main_header = soup.find('h1')

            content = self.data_organizer(mainbody_content, main_header, url)

            # content = soup.find_all('p')
            # content = [i.text for i in content]
    
            browser.close()

        return content
    
    def getting_page_content_driver(self, urls):
        for i in urls[:2]:
            if(i.get(Aws.CONTENTS.value)):
                data =  self.getting_inner_content(i['href'])
                print("\n")
                print(i["title"])
                print(i["href"])
                i[Aws.SECTIONS.value] = data
                self.getting_page_content_driver(i[Aws.CONTENTS.value])
            else:
                print(f"    |--{i["title"]}")
                print(f"        |--{i["href"]}")
                data =  self.getting_inner_content(i['href'])
                i[Aws.SECTIONS.value] = data
        return urls

        
