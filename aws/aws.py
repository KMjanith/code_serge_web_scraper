import logging
import time
import requests
from constants.aws_constants import Aws
from bs4 import BeautifulSoup
import re
from playwright.async_api import async_playwright
from utilities.utilities import Utilities

class AwsFunction:

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def __init__(self):
        pass

    # function to modify the urls to make them complete
    def make_url_hirachy(self, topic_list):
        for i in topic_list:
            if(i.get(Aws.CONTENTS.value)):
                # "content" field will consist all the content of the sub topics.
                # Hence taht section will go to the last only in the main topic section.
                # subsection recommended json hierachy will handle by the find_outer_topis function. 
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                i[Aws.SOURCE.value] = Aws.SOURCE_NAME.value
                i[Aws.PARENT_CONTENT.value] = []
                self.make_url_hirachy(i[Aws.CONTENTS.value])
            else:
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                i[Aws.SOURCE.value] = Aws.SOURCE_NAME.value
                i[Aws.PARENT_CONTENT.value] = []

    #function to find the main topics and their subtopics with the urls9
    def find_outer_topis(self):
        res = requests.get(Aws.TOPIC_URL.value)
        contents = []
        # Extract the URLs of the sections
        for i in res.json()[Aws.CONTENTS.value]:
            if i[Aws.TITLE.value] in Aws.MAIN_TOPICS.value:
                i[Aws.SOURCE.value] = Aws.SOURCE_NAME.value
                i[Aws.PARENT_CONTENT.value] = []
                i[Aws.HREF.value] = f"{Aws.BASE_URL.value}{i[Aws.HREF.value]}"
                contents.append(i)
    
        return contents
    
    # ol item handler
    def ol_handler(self, ol_item, stack):
        content = ol_item.contents
        for index,i in enumerate(content):
            if(i.name == None):
                continue
            if(i.name == Aws.LI.value):
                if(i.find(Aws.PRE.value)):
                    if(i.find(Aws.PRE.value).find(Aws.CODE.value)):
                        code = i.find(Aws.PRE.value).find(Aws.CODE.value).text.replace("anchor", "")
                        stack[-1][Aws.CONTENT.value].append(f" {index + 1} : {i.text.replace(code, ' ')}")
                        if(stack[-1][Aws.CONTENT.value][-1] == ""):
                            stack[-1][Aws.CONTENT.value].pop()
                        stack[-1][Aws.CONTENT.value].append({Aws.CODE_EXAMPLE.value: code})
                else:
                    stack[-1][Aws.CONTENT.value].append(f"  {index + 1} : {i.text.replace('\n', '')}")
                    if(stack[-1][Aws.CONTENT.value][-1] == ""):
                            stack[-1][Aws.CONTENT.value].pop()
            if(i.name == Aws.OL.value):
                self.ol_handler(i, stack)
           
        return stack
    
    # ul item handler
    def ul_handler(self, ul_item, stack):
        for index,j in enumerate(ul_item.find_all(Aws.LI.value)):
            if(j.find(Aws.P.value)):
                if(j.find(Aws.P.value).find(Aws.B.value) != None):
                    header =  j.find(Aws.B.value).text
                    stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{header} : {j.text.replace(header, '').replace("\n", '')}")
                else:
                    # there are some ul tags which don not have b tags in them becuase they don have a title in the list item
                    stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{j.text.replace("\n", '')}")    
            if(j.find(Aws.PRE.value)): 
                if(j.find(Aws.PRE.value).find(Aws.CODE.value)):
                    code = j.find(Aws.PRE.value).find(Aws.CODE.value).text
                    stack[-1][Aws.CONTENT.value].append({Aws.CODE_EXAMPLE.value: code})
                    if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                            stack[-1][Aws.CONTENT.value].pop()
        return stack
    
    # dl item handler
    def dl_handler(self, dl_item, stack):
        dt = dl_item.find_all(Aws.DT.value)
        dd = dl_item.find_all(Aws.DD.value)
        for index, j in enumerate(dt):
            if(dd[index].find(Aws.CODE.value)):
                stack[-1][Aws.CONTENT.value].append({f"{index+1} : {dt[index].text}" : {Aws.CODE_EXAMPLE.value:dd[index].find(Aws.CODE.value).text}})
                if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                    stack[-1][Aws.CONTENT.value].pop()
            else:
                stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{dt[index].text} : {dd[index].text. replace('\n', '')}")
                if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                    stack[-1][Aws.CONTENT.value].pop()
        return stack

    # div item handler
    def div_handler(self, div_item, stack):
        content = div_item.contents
        for i in content:
            if(i.name == None):
                continue

            if(i.name in Aws.DIV_MATCHING_ELEMENST.value):
                self.div_handler(i, stack)

            if(i.name == Aws.CODE.value) and (i.name != Aws.OL.value):
                code = i.find(Aws.CODE.value)
                stack[-1][Aws.CONTENT.value].append({Aws.CODE_EXAMPLE.value: code.text.replace("\n", "")})
                if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                    stack[-1][Aws.CONTENT.value].pop()

            if(i.name == Aws.PRE.value): 
                code = i.find(Aws.CODE.value)
                if(code):
                    stack[-1][Aws.CONTENT.value].append({Aws.CODE_EXAMPLE.value: code.text.replace("\n", "")})
                    if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                        stack[-1][Aws.CONTENT.value].pop()

            if(i.name == Aws.OL.value):
                self.ol_handler(i, stack)
            
            if(i.name == Aws.DL.value):
                self.dl_handler(i, stack)

            if(i.name == Aws.UL.value):
                self.ul_handler(i, stack)

            else:
                if((i.name in Aws.ITEM_LIST.value) or (i.text in Aws.ITEM_LIST.value) or (i.name in Aws.DIV_MATCHING_ELEMENST.value)):
                    continue
                else:
                    stack[-1][Aws.CONTENT.value].append(i.text.replace("\n", ""))
                    if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                        stack[-1][Aws.CONTENT.value].pop()
            
        return stack
            
    
    
    def data_organizer(self,l, main_header, url):
        stack = [{"headers":main_header, "url": url,Aws.CONTENT.value: []}]  
        original = []
        for i in l:
            if(i.name == None):
                continue
            if(i.name in Aws.TOPIC_LIST.value):
                level = int(i.name[1])
                current_stack_length = len(stack)
                if(current_stack_length < level):
                    stack.append({Aws.SUB_HEADER.value: i.text, Aws.CONTENT.value: []})
                elif(current_stack_length == level and current_stack_length != 0):
                    a = stack.pop()
                    stack[-1][Aws.CONTENT.value].append(a)
                    stack.append({Aws.SUB_HEADER.value: i.text, Aws.CONTENT.value: []})
                
                else:
                    while(len(stack) > level):
                        a = stack.pop()
                        stack[-1][Aws.CONTENT.value].append(a)
                    a = stack.pop()
                    if(len(stack)==0):
                        original.append(a)
                        stack.append({Aws.SUB_HEADER.value: i.text, Aws.CONTENT.value: []})
                    else:
                        stack[-1][Aws.CONTENT.value].append(a)
                        stack.append({Aws.SUB_HEADER.value: i.text, Aws.CONTENT.value: []})
            else:
                if(i.name == Aws.UL.value):
                    for index,j in enumerate(i.find_all(Aws.LI.value)):
                        stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{j.text.replace('\n', '')}")
                        if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                            stack[-1][Aws.CONTENT.value].pop()
                if(i.name == Aws.OL.value):
                    for index,j in enumerate(i.find_all(Aws.LI.value)):
                        stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{j.text.replace('\n', '')}")
                        if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                            stack[-1][Aws.CONTENT.value].pop()

                if(i.name == Aws.DIV.value):
                    self.div_handler(i, stack)
                    continue
                
                if(i.name == Aws.AWSDOCS_TABS.value):
                    self.div_handler(i, stack)
                    continue
            
                else:
                    if(i.name == Aws.UL.value or i.name == Aws.OL.value or i.text == "" or i.text == "\n\n" or i.name == Aws.DIV.value or i.name == Aws.AWSDOCS_TABS.value):
                        continue
                    else:
                        stack[-1][Aws.CONTENT.value].append(i.text.replace("\n", ""))
                        if(stack[-1][Aws.CONTENT.value][-1] == "anchor"):
                            stack[-1][Aws.CONTENT.value].pop()

        util = Utilities()
        return util.return_data(stack, Aws.CONTENT.value)[-1][Aws.CONTENT.value]
    
    #function to get the html content of the urls
    async def getting_inner_content(self, url, page ):

        retries = 3  # Number of retry attempts
        timeout_duration = 60000  # Timeout duration in milliseconds (60 seconds)
        attempt = 0

        while attempt < retries:
            try:
                await page.goto(url, wait_until="domcontentloaded")  # First attempt to load the page

                # Wait for the AJAX content to load (e.g., by waiting for a specific element)
                await page.wait_for_selector('main', timeout=timeout_duration)

                title_element = await page.query_selector('div#main')
                inner_html_content = await title_element.inner_html() if title_element else ""

                # Parse HTML and filter specific tags using BeautifulSoup
                soup = BeautifulSoup(inner_html_content, "html.parser")
                main_col_body = soup.find(Aws.DIV.value, id="main-col-body")
                mainbody_content = main_col_body.contents if main_col_body else []

                main_header = soup.find('h1')

                content = self.data_organizer(mainbody_content, main_header, url)

                return content
            
            except TimeoutError:
                logging.info(f"Timeout while navigating to {url}. Attempt {attempt + 1} of {retries}")
                attempt += 1
                time.sleep(2)  # Wait before retrying

                if attempt == retries:
                    logging.error(f"All attempts failed for {url}. Skipping.")
                    return None
    
        return None  # If all attempts fail
    
    async def getting_page_content_driver(self, urls):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            for i in urls:
                if(i.get(Aws.CONTENTS.value)):
                    content = await self.getting_inner_content(i[Aws.HREF.value], page)
                    logging.info(f'Main Topic :  {i[Aws.TITLE.value]}')
                    logging.info(i[Aws.HREF.value])
                    i[Aws.PARENT_CONTENT.value] = content
                    await self.getting_page_content_driver(i[Aws.CONTENTS.value])
                else:
                    logging.info(f"    |--{i[Aws.TITLE.value]}")
                    logging.info(f"        |--{i[Aws.HREF.value]}")
                    content = await self.getting_inner_content(i[Aws.HREF.value], page)
                    i[Aws.PARENT_CONTENT.value] = content
    
            await browser.close()
        
        return urls

        
