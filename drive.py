# Make a request to the React website
import json
import logging
import os
from bs4 import BeautifulSoup
import requests
from aws.aws import AwsFunction
from constants.aws_constants import Aws
from constants.react_constants import React
from constants.utility_constant import Utility
from react.react import ReactFunction
import asyncio


def structure_aws_data():
    aws_data = []
    with open(Utility.AWS_OUTPUT_FILE.value, 'r', encoding="UTF-8") as file:
        aws_data = json.load(file)

    for i in aws_data:
        parent_content = i.get(Aws.PARENT_CONTENT.value)
        if(i.get(Aws.CONTENTS.value) == None):
            i.pop(Aws.PARENT_CONTENT.value)
            i["sections"] = parent_content

        else:
            contents = i.get(Aws.CONTENTS.value)
            sections = parent_content + contents
            i.pop(Aws.PARENT_CONTENT.value)
            i.pop(Aws.CONTENTS.value )   
            i["sections"] = sections

    with open(Utility.AWS_OUTPUT_FILE.value, 'w', encoding='utf-8') as file:
        json.dump(aws_data, file, ensure_ascii=False, indent=4)

def structure_react_data():
    react_data = []
    with open(Utility.REACT_OUTPUT_FILE.value, 'r', encoding='utf-8') as file:
        react_data = json.load(file)

    for i in react_data:
        subTopics = i.get(Utility.SUBTOPICS.value)
        sections = i.get(React.SECTIONS.value)
        sections.append({"subTopics": subTopics})
        i.pop(Utility.SUBTOPICS.value)
        i["sections"] = sections

    with open(Utility.REACT_OUTPUT_FILE.value, 'w', encoding='utf-8') as file:
        json.dump(react_data, file, ensure_ascii=False, indent=4)   


def get_react_data():

    logging.info(".......***********************........")
    logging.info("           SCRAPING REACT             ")
    logging.info ("******.......................********\n")

    logging.info("Fetching data from React.dev...")
    react_response = requests.get(React.URL.value)
    react_response.raise_for_status()  # Ensure the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(react_response.text, 'html.parser')

    # Find the main topics and their subtopics with the URLs
    react = ReactFunction()

    react_result = react.find_outer_topis(soup, React.PARSING_URL.value)

    sub_topic_links = react_result[0]
    main_topic_links = react_result[1]

    # get the main page contents
    content = react.get_content_data(main_topic_links, React.MAIN.value)

    for i in range(len(content)):
        links = sub_topic_links[i][Utility.SUBTOPICS.value]
        content[i][Utility.SUBTOPICS.value] = react.get_content_data(links, "")

    with open(Utility.REACT_OUTPUT_FILE.value, 'w', encoding='utf-8') as file:
        json.dump(content, file, ensure_ascii=False, indent=4)

    print("React data saved to react.json")


def get_aws_data():
    
        logging.info(".......***********************........")
        logging.info("           SCRAPING AWS            ")
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
    
        with open(Utility.AWS_OUTPUT_FILE.value, 'w', encoding='utf-8') as file:
            json.dump(topic_urls, file, ensure_ascii=False, indent=4)
    
        logging.info("AWS data saved to aws.json\n")

        

def combining_data():
    logging.info(".......***********************........")
    logging.info("           COMBINNING DATA             ")
    logging.info ("******.......................********\n")

    # combining the data of react and aws
    try:
        combined_data = []
        json_object_list = [Utility.REACT_OUTPUT_FILE.value, Utility.AWS_OUTPUT_FILE.value]

        for json_object in json_object_list:
            with open(json_object, 'r', encoding='utf-8') as file:
                data = json.load(file)
                combined_data += data


        with open(Utility.FINAL_OUTPUT_FILE.value, 'w', encoding='utf-8') as file:
            json.dump(combined_data, file, ensure_ascii=False, indent=4)

        logging.info("Data combined and saved to original.json\n")
        logging.info(".......**********************************........")
        logging.info("         PROCESS COMPLETED SUCCESSFULLY         ")
        logging.info ("******..................................********\n")
    except json.decoder.JSONDecodeError as e:
        logging.error("one of the file content missing or try again")
        logging.error(e)
        logging.info(".......*******************........")
        logging.info("             TRY AGAIN           ")
        logging.info ("******...................********\n")


def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    get_react_data()
    structure_react_data()
    get_aws_data()
    structure_aws_data() 
    combining_data()


if __name__ == "__main__":  

    os.makedirs("outputs", exist_ok=True)

    react_file = Utility.REACT_OUTPUT_FILE.value
    aws_file = Utility.AWS_OUTPUT_FILE.value
    final_file = Utility.FINAL_OUTPUT_FILE.value

    # Check and create the output files only if they don't exist
    if not os.path.exists(react_file):
        open(react_file, 'w').close()  # create an empty json file for react

    if not os.path.exists(aws_file):
        open(aws_file, 'w').close()  # create an empty json file for aws

    if not os.path.exists(final_file):
        open(final_file, 'w').close()  # create an empty json file for final output

    # Run the main function
    main()