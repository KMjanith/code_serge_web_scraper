# Make a request to the React website
import json
import logging
from bs4 import BeautifulSoup
import requests
from aws.aws import AwsFunction
from constants.aws_constants import Aws
from constants.react_constants import React
from react.react import ReactFunction

SUBTOPICS = "subTopics"
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


# logging.info(".......***********************........")
# logging.info("           SCRAPING REACT             ")
# logging.info ("******.......................********\n")
# logging.info("Fetching data from React.dev...")


# react_response = requests.get(React.URL.value)
# react_response.raise_for_status()  # Ensure the request was successful

# logging.info("Data fetched successfully")

# logging.info("Parsing data please wait.....")
# # Parse the HTML content
# soup = BeautifulSoup(react_response.text, 'html.parser')

# # Find the main topics and their subtopics with the URLs
# react = ReactFunction()
# aws = AwsFunction()

# logging.info("getting all the topics and subtopics")
# react_result = react.find_outer_topis(soup, React.PARSING_URL.value)

# sub_topic_links = react_result[0]
# main_topic_links = react_result[1]

# logging.info("Structuring the main pages' data")

# # get the main page contents
# content = react.get_content_data(main_topic_links, React.MAIN.value)

# logging.info("Structuring the subtopics data")

# for i in range(len(content)):
#     links = sub_topic_links[i]["subTopics"]
#     content[i]["subTopics"] = react.get_content_data(links, "")

# logging.info("Data parsed successfully")

# output_file = "./outputs/react.json"

# with open(output_file, 'w', encoding='utf-8') as file:
#     json.dump(content, file, ensure_ascii=False, indent=4)

# logging.info("React data saved to react.json") 

logging.info("""
\n.......***********************........
            SCRAPING AWS             
"******.......................********\n""")


aws = AwsFunction()
logging.info("Fetching data from AWS...")

#getting aws side bar topics and urls
topic_urls = aws.find_outer_topis()

logging.info("Making Topic , subTopic hiraachy")

# making the parent child side bar content hirachy
for topic in topic_urls:
    if(topic.get(Aws.CONTENTS.value)):
        aws.make_url_hirachy(topic[Aws.CONTENTS.value])
    else:
        topic[Aws.SECTIONS.value] = []


logging.info("Getting and Structering data from the urls")
# getting the html content of the urls
topic_urls = aws.getting_page_content_driver(topic_urls)

output_file = "./outputs/aws.json"

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(topic_urls, file, ensure_ascii=False, indent=4)

logging.info("AWS data saved to aws.json")










