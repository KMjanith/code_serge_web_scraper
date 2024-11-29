from enum import Enum

class Aws(Enum):
    TOPIC_URL = "https://docs.aws.amazon.com/lambda/latest/dg/toc-contents.json"
    BASE_URL = "https://docs.aws.amazon.com/lambda/latest/dg/"

    NAV = "nav"
    LI = "li"
    UL = "ul"
    OL = "ol"
    DL = "dl"
    A = "a"
    P = "p"
    B = "b"
    DT = "dt"
    DD = "dd"
    DIV = "div"
    HREF = "href"
    URL = "url"
    SOURCE = "source"
    MAIN = "main"
    TITLE = "title"
    CODE = "code"
    PRE = "pre"
    TOPIC_LIST = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']  
    ITEM_LIST = ["ul" ,"ol" ,"dl","" ,"\n\n" ,'div' ,'pre'] 

    CONTENT = "content"
    CONTENTS = "contents"
    PARENT_CONTENT = "parent_content"   
    DIV_MATCHING_ELEMENST = [ "div" , 'awsui-expandable-section'  , 'awsdocs-tabs']
    AWSDOCS_TABS = 'awsdocs-tabs'
    CODE_EXAMPLE = "code_example"
    SUB_HEADER = "sub_header"   
   
    SOURCE_NAME = "Aws"
    MAIN_TOPICS = [
            "What is AWS Lambda?",
            "Example apps",
            "Building with TypeScript",
            "Integrating other services",
            "Code examples"
        ]
   


    