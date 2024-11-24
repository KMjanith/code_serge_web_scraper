# Make a request to the React website
import json
from bs4 import BeautifulSoup
import requests
from constants import React
from react import ReactFunction


print("Fetching data from React.dev...")


main_data_list =  []

response = requests.get(React.URL.value)
response.raise_for_status()  # Ensure the request was successful

print("Data fetched successfully")
print("Parsing data please wait.....")
# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

# Find the main topics and their subtopics with the URLs
react = ReactFunction()

print("getting all the topics and subtopics")
result = react.find_outer_topis(soup, React.PARSING_URL.value)

sub_topic_links = result[0]
main_topic_links = result[1]

print("getting the main pages' data")

# get the main page contents
content = react.get_content_data(main_topic_links, React.MAIN.value)

print("getting the subtopics data")

for i in range(len(content)):
    links = sub_topic_links[i]["subTopics"]
    content[i]["subTopics"] = react.get_content_data(links, "")

print("Data parsed successfully")

#extract links from json
# links = react. extract_links_from_json(result[0])


output_file = "original.json"

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(content, file, ensure_ascii=False, indent=4)

print("Data saved to original.json")

