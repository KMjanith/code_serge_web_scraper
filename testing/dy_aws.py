import json
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from constants.aws_constants import Aws
from utilities.utilities import Utilities

class DY_AWS:

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
        stack = [{Aws.HEADERS.value:main_header, "url": url,Aws.CONTENT.value: []}]  
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
                if(i.name == 'ul'):
                    for index,j in enumerate(i.find_all(Aws.LI.value)):
                        stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{j.text}")
                if(i.name == 'ol'):
                    for index,j in enumerate(i.find_all(Aws.LI.value)):
                        stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{j.text}")

                if(i.name == 'div'):
                    code = i.find('code')

                    if(code):
                        stack[-1][Aws.CONTENT.value].append({Aws.CODE_EXAMPLE.value: code.text})

                    if(i.find('dl')):
                        dl = i.find('dl')
                        dt = dl.find_all('dt')
                        dd = dl.find_all('dd')
                        for index, j in enumerate(dt):
                            if(dd[index].find('code')):
                                stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{dt[index].text} : {dd[index].find('code').text}")
                            else:
                                stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{dt[index].text} : {dd[index].text}")


                    if(i.find('ul')):
                        for index,j in enumerate(i.find_all(Aws.LI.value)):
                            if(j.find('p')):
                                if(j.find('p').find("b") != None):
                                    header =  j.find("b").text
                                    stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{header} : {j.text.replace(header, '').replace("\n", '')}")
                                else:
                                    # there are some ul tags which don not have b tags in them becuase they don have a title in the list item
                                    stack[-1][Aws.CONTENT.value].append(f"  {index+1}.{j.text.replace("\n", '')}")    
                            if(j.find('pre')): 
                                if(i.find('pre').find('code')):
                                    code = i.find('pre').find('code')
                                    stack[-1][Aws.CONTENT.value].append({Aws.CODE_EXAMPLE.value: code.text})
                            

                    else:
                        stack[-1][Aws.CONTENT.value].append(i.text)
            
                else:
                    if(i.name == "ul" or i.name == "ol" or i.text == "" or i.text == "\n\n" or i.name == 'div'):
                        continue
                    else:
                        stack[-1][Aws.CONTENT.value].append(i.text.replace("\n", ""))

        util = Utilities()
        return util.return_data(stack, Aws.CONTENT.value)[-1][Aws.CONTENT.value]
    
    #function to get the html content of the urls
    def getting_inner_content(self, url):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(url, wait_until="domcontentloaded")  # Load the page

            try:
                page.goto(url, timeout=60000)
            except TimeoutError:
                print(f"Timeout while navigating to {url}")
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
                print(f'Main Topic :  {i["title"]}')
                print(i["href"])
                i[Aws.SECTIONS.value] = data
                self.getting_page_content_driver(i[Aws.CONTENTS.value])
            else:
                print(f"    |--{i["title"]}")
                print(f"        |--{i["href"]}")
                data =  self.getting_inner_content(i['href'])
                i[Aws.SECTIONS.value] = data
        return urls

        
print("\n.......***********************........")
print("             SCRAPING AWS             ")
print ("******.......................********\n")


aws = DY_AWS()
print("Fetching data from AWS...")


print("Getting and Structering data from the urls")
# getting the html content of the urls
topic_urls = aws.getting_page_content_driver([{
        "title": "What is AWS Lambda?",
        "href":"https://docs.aws.amazon.com/lambda/latest/dg/typescript-package.html",
        "sections": []
    }])

output_file = "./outputs/aws.json"

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(topic_urls, file, ensure_ascii=False, indent=4)

print("AWS data saved to aws.json")