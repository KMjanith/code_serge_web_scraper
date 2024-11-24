# Make a request to the React website
import json
from bs4 import BeautifulSoup
import requests
from aws.aws import AwsFunction
from aws.aws_constants import Aws
from react.react_constants import React
from react.react import ReactFunction


# print("Fetching data from React.dev...")


# react_response = requests.get(React.URL.value)
# react_response.raise_for_status()  # Ensure the request was successful

# print("Data fetched successfully")
# print("Parsing data please wait.....")
# # Parse the HTML content
# soup = BeautifulSoup(react_response.text, 'html.parser')

# # Find the main topics and their subtopics with the URLs
# react = ReactFunction()
# aws = AwsFunction()

# print("getting all the topics and subtopics")
# react_result = react.find_outer_topis(soup, React.PARSING_URL.value)



# sub_topic_links = react_result[0]
# main_topic_links = react_result[1]

# print("getting the main pages' data")

# # get the main page contents
# content = react.get_content_data(main_topic_links, React.MAIN.value)

# print("getting the subtopics data")

# for i in range(len(content)):
#     links = sub_topic_links[i]["subTopics"]
#     content[i]["subTopics"] = react.get_content_data(links, "")

# print("Data parsed successfully")

# output_file = "react.json"

# with open(output_file, 'w', encoding='utf-8') as file:
#     json.dump(content, file, ensure_ascii=False, indent=4)

# print("React data saved to react.json")

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://docs.aws.amazon.com/lambda/latest/dg/welcome.html")

    # Wait for the AJAX content to load (e.g., by waiting for a specific element)
    # page.wait_for_selector('main', timeout=60000)  # Wait for dynamic content for up to 60 seconds

    # # Extract content
    # content = page.inner_text('main')  # Replace with the actual selector
    # print(content)

    title_element = page.query_selector('div#main')
    print(title_element.inner_text())
    # for i in title_element:
    #     print("Title:", i.inner_text())
    

    browser.close()

# asw = AwsFunction()
# print("Fetching data from AWS...")

# topic_urls = asw.find_outer_topis()

# for topic in topic_urls:
#     if(topic.get("contents")):
#         asw.make_url_hirachy(topic["contents"])
#     else:
#         topic["sections"] = []

# with open("aws-test.json", 'w', encoding='utf-8') as file:
#     json.dump(topic_urls, file, ensure_ascii=False, indent=4)









