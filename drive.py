# Make a request to the React website
import json
from bs4 import BeautifulSoup
import requests
from aws.aws import AwsFunction
from constants.aws_constants import Aws
from constants.react_constants import React
from react.react import ReactFunction



print("Fetching data from React.dev...")


react_response = requests.get(React.URL.value)
react_response.raise_for_status()  # Ensure the request was successful

print("Data fetched successfully")
print("Parsing data please wait.....")
# Parse the HTML content
soup = BeautifulSoup(react_response.text, 'html.parser')

# Find the main topics and their subtopics with the URLs
react = ReactFunction()
aws = AwsFunction()

print("getting all the topics and subtopics")
react_result = react.find_outer_topis(soup, React.PARSING_URL.value)



sub_topic_links = react_result[0]
main_topic_links = react_result[1]

print("getting the main pages' data")

# get the main page contents
content = react.get_content_data(main_topic_links, React.MAIN.value)

print("Getting the subtopics data")

for i in range(len(content)):
    links = sub_topic_links[i]["subTopics"]
    content[i]["subTopics"] = react.get_content_data(links, "")

print("Data parsed successfully")

output_file = "./outputs/react.json"

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(content, file, ensure_ascii=False, indent=4)

print("React data saved to react.json")



# aws = AwsFunction()
# print("Fetching data from AWS...")

# #getting aws side bar topics and urls
# topic_urls = aws.find_outer_topis()

# # making the parent child side bar content hirachy
# for topic in topic_urls:
#     if(topic.get(Aws.CONTENTS.value)):
#         aws.make_url_hirachy(topic[Aws.CONTENTS.value])
#     else:
#         topic[Aws.SECTIONS.value] = []

# # getting the html content of the urls
# topic_urls = aws.getting_page_content_driver(topic_urls)


# with open("./outputs/aws.json", 'w', encoding='utf-8') as file:
#     json.dump(topic_urls, file, ensure_ascii=False, indent=4)











