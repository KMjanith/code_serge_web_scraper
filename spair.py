import json
from bs4 import BeautifulSoup
import requests

def process_content_divs(content_divs):
    
    stack = [{"header": "", "content": []}]
    current_inputter = stack[-1]["content"]
    header = ""

    for index, div in enumerate(content_divs[:3]):
        # Extract headers and subheaders
        content = div.contents
        for i in content:
            if i.name == None:
                continue
            if(i.name == 'div'):
                code = i.find('code')
                if(code):
                    current_inputter.append({"code_example": code.text})
                else:
                    print(i.text)
                    current_inputter.append(i.text)
            if i.name == 'h4':
                if(header == 'h4'):
                    current_inputter = stack[-1]["content"]
                    current_inputter.append({"subheader": i.text, "content": []})
                    current_inputter = current_inputter[-1]["content"]
                    header = 'h4'
                else:
                    current_inputter.append({"subheader": i.text, "content": []})
                    current_inputter = current_inputter[-1]["content"]
                    header = 'h4'
            if i.name in ['h1', 'h2', 'h3']:
                if i.text:
                    stack.append({"header": i.text, "content": []})
                    current_inputter = stack[-1]["content"]
                    header = i.text
            if(i.name == 'ul'):
                for index,j in enumerate(i.find_all('li')):
                    current_inputter.append(f"  {index+1}.{j.text}")
            if(i.name == 'ol'):
                for index,j in enumerate(i.find_all('li')):
                    current_inputter.append(f"  {index+1}.{j.text}")
            else:
                if(i.name == "ul" or i.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] or i.name == 'div'):
                    continue
                if i.text:
                    print(i.name)
                    
                    current_inputter.append(i.text)
   
    return stack



# Fetch the web page
url = "https://react.dev/learn/tutorial-tic-tac-toe"
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

soup = BeautifulSoup(response.text, 'html.parser')

# Locate the main content
outer_div = soup.find('main')
all_div_in_article = outer_div.find('article').find('div', class_="max-w-7xl mx-auto")

# Find all content divs and code/picture divs
content_divs = all_div_in_article.find_all('div', class_="max-w-4xl ms-0 2xl:mx-auto")
codes_with_pictures = all_div_in_article.find_all('div', class_="sandpack sandpack--playground w-full my-8")

# Process the content divs to build the hierarchy
hierarchy = process_content_divs(content_divs)

output_file = "content_hierarchy.json"
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(hierarchy, file, ensure_ascii=False, indent=4)

print(f"Data successfully written to {output_file}")