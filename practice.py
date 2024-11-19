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


# Send a GET request to fetch the webpage content
response = requests.get(React.URL.value)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

link_results = find_outer_topis(soup, React.PARSING_URL.value)
json_content = json.dumps(link_results, indent=4)
print(json_content)

