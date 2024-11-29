# Make a request to the React website
import json
import logging
from bs4 import BeautifulSoup
import requests
from aws.aws import AwsFunction
from constants.aws_constants import Aws
from constants.react_constants import React
from react.react import ReactFunction
import asyncio

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

logging.info(".......***********************........")
logging.info("           SCRAPING Aws            ")
logging.info("******.......................********\n")


aws = AwsFunction()
logging.info("Fetching urls from AWS...")

#getting aws side bar topics and urls
topic_urls = aws.find_outer_topis()

logging.info("Making Topic , subTopic hiraachy")

# making the parent child side bar content hirachy
for topic in topic_urls:
    if(topic.get(Aws.CONTENTS.value)):
        aws.make_url_hirachy(topic[Aws.CONTENTS.value])
    else:
        topic[Aws.PARENT_CONTENT.value] = []



logging.info("Getting and Structering data from the urls")
# getting the html content of the urls
topic_urls = asyncio.run(aws.getting_page_content_driver(topic_urls))

for i in topic_urls:
    # "content" field will consist all the content of the sub topics.
    # Hence taht section will go to the last only in the main topic section.
    # subsection recommended json hierachy will handle by the find_outer_topis function. 
    if(i.get(Aws.CONTENTS.value)):
        temp_content = i[Aws.CONTENTS.value]
        i[Aws.CONTENTS.value] = temp_content


output_file = "./outputs/aws.json"

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(topic_urls, file, ensure_ascii=False, indent=4)

logging.info("AWS data saved to aws.json\n")


# Combining scraped react data and the aws data into one json file
# content will save to the `./outputs/original.json` file

logging.info(".......***********************........")
logging.info("           COMBINNING DATA             ")
logging.info ("******.......................********\n")

# combining the data of react and aws
combined_data = []
json_object_list = ['outputs/react.json', 'outputs/aws.json']

for json_object in json_object_list:
    with open(json_object, 'r') as file:
        data = json.load(file)
        combined_data.append(data)

output_file = "./outputs/original.json"

with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(combined_data, file, ensure_ascii=False, indent=4)

logging.info("Data combined and saved to original.json\n")

logging.info(".......***********************........")
logging.info("      Process completed successfully      ")
logging.info ("******.......................********\n")










