# code_serge_web_scraper

## install the dependencies
```
pip install -r requirements.txt
```

## install playwrite
```
playright install
```

## to run the program
```
python drive.py
```

## if you get
ModuleNotFoundError: No module named bs4
try
```
pip install beautifulsoup4
```

## then try again
```
python drive.py
```

## you can see 3 .json files with the output
1. react.json
2. aws.json
3. final_result.json

the final_result.json has the combined result of the both scraped contents

## if you want to scrape documentations sepreately
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

