from enum import Enum

class Aws(Enum):
    TOPIC_URL = "https://docs.aws.amazon.com/lambda/latest/dg/toc-contents.json"
    BASE_URL = "https://docs.aws.amazon.com/lambda/latest/dg/"
    NAV = "nav"
    LI = "li"
    UL = "ul"
    A = "a"
    DIV = "div"
    HREF = "href"
    MAIN = "main"
    CONTENTS = "contents"
    SECTIONS = "sections"   
    TITLE = "title"
    TOPIC_LIST = ['h1', 'h2', 'h3', 'h4']
    MAIN_TOPICS = [
            "What is AWS Lambda?",
            "Example apps",
            "Building with TypeScript",
            "Integrating other services",
            "Code examples"
        ]


    