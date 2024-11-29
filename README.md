# Code_serge_web_scraper

## Tnstall the dependencies
```
pip install -r requirements.txt
```

## Install playwrite
```
playright install
```

## To run the program
```
python drive.py
```

## If you get
ModuleNotFoundError: No module named bs4
try
```
pip install beautifulsoup4
```

## Then try again
```
python drive.py
```

## You can see 3 .json files with the output
1. react.json
2. aws.json
3. final_result.json

the final_result.json has the combined result of the both scraped contents

## If you want to scrape documentations sepreately
1. go to drive.py
2. comment out follwoign lines as you want in the main function 
```
get_react_data()
structure_react_data()
get_aws_data()
structure_aws_data() 
combining_data()
```
3. if you scraping individual documentations it is good to comment out the `combining_data()` line.

# JSON hierachies

### aws.json
```
{[
   "title": main_header,
   "source":"aws_lambda ,
   "url": url_of_the_page ,
   "contents": [content os the sub pages], 
   "parent_content": [content of the main page]
]}
```

### react.json

``` 
{[
   "title": main_header,
   "source": "react",
   "url": url_of_the_page ,
   "sections": [content of the main page], 
   "subTopics": [sub pages and their content]
 ]}
 ```

 ### final_result.json
 ```
 {[
    "title": title of the page,
    "url": page url,
    "source": "aws_lamda"| "react",
    "sections" : []

 ]}