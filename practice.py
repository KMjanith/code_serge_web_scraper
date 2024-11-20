import json
import requests
from constants import React
from bs4 import BeautifulSoup

def find_outer_topis(soup, url):
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
            result[main_sub_topic][j.find(React.A.value).text] ={
                "url": subtopic_url, "main_page_sub_topics": [{"title": "", "url": "", "notes": "", "code_snippets": ""}]}
    return result

def getting_inner_content(url):

    # Find all headers in order
    headers = soup.find("main").find("article").find_all(['h1', 'h2', 'h3', 'h4'])

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

            if sibling.name in ['h1', 'h2', 'h3', 'h4'] and int(sibling.name[1]) <= tag_level:
                break  # Stop at the next header of the same or higher level
            if sibling.name == 'div':  # Detect <code> tags
                code_snippets.append(sibling.get_text(strip=True)) 
            elif sibling.name and sibling.get_text(strip=True):  # Only include non-empty text
                siblings.append(sibling.get_text(strip=True))

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

response = requests.get(React.URL.value)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

#link_results = find_outer_topis(soup, React.PARSING_URL.value)
#json_content = json.dumps(link_results, indent=4)
#print(json_content)

url = "https://react.dev/learn/tutorial-tic-tac-toe"
json_content = getting_inner_content(url)
print(json_content)





