import logging
import requests
from constants.react_constants import React
from bs4 import BeautifulSoup
from utilities.utilities import Utilities

class ReactFunction:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    def __init__(self):
        pass

    #function to find the main topics and their subtopics with the urls
    def find_outer_topis(self,soup, url):
        aside = soup.find(React.ASIDE.value)
        nav = aside.find(React.NAV.value)
        all_li = nav.find_all(React.LI.value)
        outer_li = [li for li in all_li if li.find(React.UL.value)]

        #dictionary to store the main topics
        main_topic = []
        for index,i in enumerate(outer_li):
            a = i.find(React.A.value)
            url_main_topics  = a.get(React.HREF.value)
            main_topic.append({"topic": a.text , "url":url + url_main_topics}) 

        #dictionary to store the toic hirachy
        result = []
        for i in outer_li:
            main_sub_topic = i.find(React.A.value).find(React.DIV.value).text   #main sub topics in aside nav bar
            temp_dic = {"topic": main_sub_topic, "subTopics": []}
            inner_li = i.find(React.UL.value).find_all(React.LI.value)
            temp = []

            # getting sub topics and their urls for the main sub topics
            for j in inner_li:
                subtopic_url = url + j.find(React.A.value).get(React.HREF.value)
                temp.append({"topic": j.find(React.A.value).text, "url": subtopic_url})
            temp_dic["subTopics"] = temp
            result.append(temp_dic)
        return [result, main_topic]
    
    
    def sub_heddings_data_collector(self,l, main_header, url, util):
        stack = [{"headers":main_header, "url": url,React.CONTENT.value: []}]  
        original = []
        for i in l:
            if(i.name == None):
                continue
            if(i.name in React.TOPIC_LIST.value):
                level = int(i.name[1])
                current_stack_length = len(stack)
                if(current_stack_length < level):
                    sub_url = i.find(React.A.value)
                    stack.append({React.SUBHEADER.value: i.text, "source":React.SOURCE.value,"url": f"{url}/{sub_url.get('href')}",React.CONTENT.value: []})
                elif(current_stack_length == level and current_stack_length != 0):
                    a = stack.pop()
                    stack[-1][React.CONTENT.value].append(a)
                    sub_url = i.find(React.A.value)
                    stack.append({React.SUBHEADER.value: i.text,"source":React.SOURCE.value, "url": f"{url}/{sub_url.get('href')}",React.CONTENT.value: []})
                
                else:
                    while(len(stack) > level):
                        a = stack.pop()
                        stack[-1][React.CONTENT.value].append(a)
                    a = stack.pop()
                    if(len(stack)==0):
                        original.append(a)
                        sub_url = i.find(React.A.value)
                        stack.append({React.SUBHEADER.value: i.text,"source":React.SOURCE.value, "url": f"{url}/{sub_url.get('href')}",React.CONTENT.value: []})
                    else:
                        stack[-1][React.CONTENT.value].append(a)
                        sub_url = i.find(React.A.value)
                        stack.append({React.SUBHEADER.value: i.text, "source":React.SOURCE.value,"url": f"{url}/{sub_url.get('href')}",React.CONTENT.value: []})
            else:
                if(i.name == React.UL.value):
                    for index,j in enumerate(i.find_all(React.LI.value)):
                        stack[-1][React.CONTENT.value].append(f"  {index+1}.{j.text}")
                if(i.name == React.OL.value):
                    for index,j in enumerate(i.find_all(React.LI.value)):
                        stack[-1][React.CONTENT.value].append(f"  {index+1}.{j.text}")
                
                if(i.name == React.DIV.value):
                    try:
                        code = i.find('code')
                        if(code and (stack[-1][React.CONTENT.value][-1] != {"code_example": code.text})):
                            stack[-1][React.CONTENT.value].append({"code_example": code.text})
                        if(i.get('class')[1] == 'sandpack--playground'):
                            code_sandbox = util.remove_redundant(i.text)
                            stack[-1][React.CONTENT.value].append({"code_sandbox": code_sandbox})
                        else:
                            if(i.find(React.UL.value)):
                                for index,j in enumerate(i.find_all(React.LI.value)):
                                    stack[-1][React.CONTENT.value].append(f"  {index+1}.{j.text}")
                            if(i.find(React.OL.value)):
                                for index,j in enumerate(i.find_all(React.LI.value)):
                                    stack[-1][React.CONTENT.value].append(f"  {index+1}.{j.text}")
                            else:
                                if(i.name == "ul" or i.name == "ol" or i.find('code') or i.find('img')):
                                    continue
                                else:
                                    stack[-1][React.CONTENT.value].append(i.text)
                    except: IndexError
                   
            
                else:
                    if(i.name == "ul" or i.name == "ol" or i.name == "div" or i.name == "img"):
                        continue
                    else:
                        stack[-1][React.CONTENT.value].append(i.text)

        return util.return_data(stack, React.CONTENT.value)
    
    
    def main_heading_data_collector(self, page_item_list, main_header, url, util):

        stack = [{"title": main_header,"source": React.SOURCE.value ,"url": url,React.SECTIONS.value: [], "subTopics": []}]
        original = []
        for i in page_item_list:
            if(i.name == None):
                continue
            if(i.name in React.TOPIC_LIST.value):
                level = int(i.name[1])
                current_stack_length = len(stack)
                if(current_stack_length < level):
                    sub_url = i.find(React.A.value)
                    if(sub_url):
                        stack.append({"subHeader": i.text, "url": f"{url}/{sub_url.get('href')}",React.SECTIONS.value: [] })
                elif(current_stack_length == level and current_stack_length != 0):
                    a = stack.pop()
                    stack[-1][React.SECTIONS.value].append(a)
                    sub_url = i.find(React.A.value)
                    if(sub_url):
                        stack.append({"subHeader": i.text, "url": f"{url}/{sub_url.get('href')}",React.SECTIONS.value: [] })
                
                else:
                    while(len(stack) > level):
                        a = stack.pop()
                        stack[-1][React.SECTIONS.value].append(a)
                    a = stack.pop()
                    if(len(stack)==0):
                        original.append(a)
                        sub_url = i.find(React.A.value)
                    if(sub_url):
                        stack.append({"subHeader": i.text, "url": f"{url}/{sub_url.get('href')}",React.SECTIONS.value: [] })
                    else:
                        stack[-1][React.SECTIONS.value].append(a)
                        sub_url = i.find(React.A.value)
                    if(sub_url):
                        stack.append({"subHeader": i.text, "url": f"{url}/{sub_url.get('href')}",React.SECTIONS.value: [] })
            else:
                if(i.name == React.UL.value):
                    for index,j in enumerate(i.find_all(React.LI.value)):
                        stack[-1][React.SECTIONS.value].append(f"  {index+1}.{j.text}")
                if(i.name == React.OL.value):
                    for index,j in enumerate(i.find_all(React.LI.value)):
                        stack[-1][React.SECTIONS.value].append(f"  {index+1}.{j.text}")

                if(i.name == 'div'):
                    
                    try:
                        code = i.find('code')
                        if(code and (stack[-1][React.SECTIONS.value][-1] != {"code_example": code.text})):
                            stack[-1][React.SECTIONS.value].append({"code_example": code.text})
                        if(i.get('class')[1] == 'sandpack--playground'):
                            code_sandbox = util.remove_redundant(i.text)
                            stack[-1][React.SECTIONS.value].append({"code_sandbox": code_sandbox})
                        else:
                            if(i.find(React.UL.value)):
                                for index,j in enumerate(i.find_all(React.LI.value)):
                                    stack[-1][React.SECTIONS.value].append(f"  {index+1}.{j.text}")
                            if(i.find(React.OL.value)):
                                for index,j in enumerate(i.find_all(React.LI.value)):
                                    stack[-1][React.SECTIONS.value].append(f"  {index+1}.{j.text}")
                            else:
                                if(i.name == "ul" or i.name == "ol" or i.find('code') or i.find('img')):
                                    continue
                                else:
                                    stack[-1][React.SECTIONS.value].append(i.text)
                    except: IndexError
                
            
                else:
                    if(i.name == "ul" or i.name == "ol" or i.name == "div" or i.name == "img"):
                        continue
                    else:
                        stack[-1][React.SECTIONS.value].append(i.text)

        return util.return_data(stack, React.SECTIONS.value)


    #function to get the inner content of the urls
    def getting_inner_content(self,url, main_or_sub):
        util = Utilities()
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all sub headers in order
        #headers = soup.find("main").find("article").find_all(React.TOPIC_LIST.value)

        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # getting page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the main content
        outer_div = soup.find('main')

        # Extracting the article content
        article = outer_div.find('article').find("div", class_="ps-0")

        # Extracting the inner content of the article
        inner_content = article.contents

        #main header
        h1 = inner_content[0]
        h1 = h1.find_all('h1')
        h1 = h1[0].text

        # Extracting the data from the inner content 
        data = inner_content[1]

        # Extracting the actual data from the data,2nd item is the footer
        actual_data = data.contents[0]  

        divs = actual_data.contents
        all_divs = []
        for i in divs:
            if(i.name == None):
                continue
            else:
                all_divs.append(i)
            
        # Extracting all the divs from the actual data
        # all_divs = actual_data.find_all('div', class_="max-w-4xl ms-0 2xl:mx-auto")

        # Extract items with the div and make the list with inner content
        page_item_list = util.make_item_list(all_divs)

        if(main_or_sub == React.MAIN.value):
            # getting main page data
            main_pages = self.main_heading_data_collector(page_item_list, h1, url, util)
            return main_pages
        else:
            # getting sub page data
            sub_pages = self.sub_heddings_data_collector(page_item_list, h1, url, util)
            return sub_pages


    #function to extract the urls from the json content
    def extract_links_from_json(self,json_content):
        links = []
        for key, value in json_content.items():
            for sub_key, sub_value in value.items():
                links.append(sub_value["url"])
        return links

    def get_content_data(self,link_list, main_or_sub):
        body_content = []
        for link in link_list:
            logging.info(f"-------Getting data from {link['url']}")
            original_dict = self.getting_inner_content(link["url"], main_or_sub)
            body_content.append(original_dict[0])
        return body_content 
    





