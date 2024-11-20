# Make a request to the React website
import json
from bs4 import BeautifulSoup
import requests
from constants import React
from react import ReactFunction
import imoji

print("Fetching data from React.dev...")

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

#extract links from json
links = react. extract_links_from_json(result)

print("getting the data ...")

# get the page contents
content = react.get_cotent_data(links)

