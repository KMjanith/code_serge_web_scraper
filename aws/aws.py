import logging
import requests
from constants.aws_constants import Aws
from bs4 import BeautifulSoup
import re
from playwright.sync_api import sync_playwright
from utilities.utilities import Utilities

class AwsFunction:

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def __init__(self):
        pass

    # function to modify the urls to make them complete
    def make_url_hirachy(self, topic_list):
        for i in topic_list:
            if(i.get(Aws.CONTENTS.value)):
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                i[Aws.SOURCE.value] = "Aws"
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
    
    # ol item handler
    def ol_handler(self, ol_item, stack):
        content = ol_item.contents
        for index,i in enumerate(content):
            if(i.name == None):
                continue
            if(i.name == 'li'):
                if(i.find('pre')):
                    if(i.find('pre').find('code')):
                        code = i.find('pre').find('code').text
                        stack[-1]["content"].append(f"  {i.text.replace(code, ' ')}")
                        stack[-1]["content"].append({"code_example": code})
                else:
                    stack[-1]["content"].append(f"  {index + 1} : {i.text.replace('\n', '')}")
            if(i.name == 'ol'):
                stack = self.ol_handler(i, stack)
           
        return stack
    
    # ul item handler
    def ul_handler(self, ul_item, stack):
        for index,j in enumerate(ul_item.find_all('li')):
            if(j.find('p')):
                if(j.find('p').find("b") != None):
                    header =  j.find("b").text
                    stack[-1]["content"].append(f"  {index+1}.{header} : {j.text.replace(header, '').replace("\n", '')}")
                else:
                    # there are some ul tags which don not have b tags in them becuase they don have a title in the list item
                    stack[-1]["content"].append(f"  {index+1}.{j.text.replace("\n", '')}")    
            if(j.find('pre')): 
                if(j.find('pre').find('code')):
                    code = j.find('pre').find('code').text
                    stack[-1]["content"].append({"code_example": code})
        return stack
    
    # dl item handler
    def dl_handler(self, dl_item, stack):
        dt = dl_item.find_all('dt')
        dd = dl_item.find_all('dd')
        for index, j in enumerate(dt):
            if(dd[index].find('code')):
                stack[-1]["content"].append(f"  {index+1}.{dt[index].text} : {dd[index].find('code').text}")
            else:
                stack[-1]["content"].append(f"  {index+1}.{dt[index].text} : {dd[index].text}")
        return stack

    # div item handler
    def div_handler(self, div_item, stack):
        content = div_item.contents
        for i in content:
            if(i.name == None):
                continue

            if(i.name == 'div' or i.name == 'awsui-expandable-section' or i.name == 'awsdocs-tabs'):
                self.div_handler(i, stack)

            if(i.name == 'code') and (i.name != 'ol'):
                code = i.find('code')
                stack[-1]["content"].append({"code_example": code.text})

            if(i.name == 'pre'): 
                code = i.find('code')
                if(code):
                    stack[-1]["content"].append({"code_example": code.text})

            if(i.name == 'ol'):
                stack = self.ol_handler(i, stack)
            
                        
            if(i.name == 'dl'):
                stack = self.dl_handler(i, stack)

            if(i.name == 'ul'):
                stack = self.ul_handler(i, stack)

            else:
                if(i.name == "ul" or i.name == "ol" or i.text == "" or i.text == "\n\n" or i.name == 'div' or i.name == 'pre'):
                    continue
                else:
                    stack[-1]["content"].append(i.text.replace("\n", ""))
            
        return stack
            
    
    
    def data_organizer(self,l, main_header, url):
        stack = [{"headers":main_header, "url": url,"content": []}]  
        original = []
        for i in l:
            if(i.name == None):
                continue
            if(i.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
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
                    stack = self.div_handler(i, stack)
                
                if(i.name == 'awsdocs-tabs'):
                    stack = self.div_handler(i, stack)
            
                else:
                    if(i.name == "ul" or i.name == "ol" or i.text == "" or i.text == "\n\n" or i.name == 'div'):
                        continue
                    else:
                        stack[-1]["content"].append(i.text.replace("\n", ""))

        util = Utilities()
        return util.return_data(stack, "content")[-1]['content']
    
    #function to get the html content of the urls
    def getting_inner_content(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")  # Load the page

            try:
                page.goto(url, timeout=60000)
            except TimeoutError:
                logging.info(f"Timeout while navigating to {url}")
                return None  # Or handle the failure appropriately
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
    
            browser.close()

        return content
    
    def getting_page_content_driver(self, urls):
        for i in urls:
            if(i.get(Aws.CONTENTS.value)):
                data =  self.getting_inner_content(i['href'])
                logging.info(f'Main Topic :  {i["title"]}')
                logging.info(i["href"])
                i[Aws.SECTIONS.value] = data
                self.getting_page_content_driver(i[Aws.CONTENTS.value])
            else:
                logging.info(f"    |--{i["title"]}")
                logging.info(f"        |--{i["href"]}")
                data =  self.getting_inner_content(i['href'])
                i[Aws.SECTIONS.value] = data
        return urls

        
