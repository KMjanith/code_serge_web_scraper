l = ['h1', 'h2', '1','2', 'h3', '3', 'h3', '4', 'h4', '5', 'h2', '6', 'h1', '7']

def stack(l, main_header):
    stack = [{"headers":main_header, "content": []}]  
    original = []
    for i in l:
        if(i.name == None):
            continue
        # print(stack)
        # print("tag: ", i.name)
        # print("data: ", i.text) 
        # print("\n")
        if(i.name in ['h1', 'h2', 'h3', 'h4']):
            level = int(i.name[1])
            current_stack_length = len(stack)
            if(current_stack_length < level):
                stack.append({"header": i.text, "content": []})
            elif(current_stack_length == level and current_stack_length != 0):
                a = stack.pop()
                stack[-1]["content"].append(a)
                stack.append({"header": i.text, "content": []})
            
            else:
                while(len(stack) > level):
                    a = stack.pop()
                    stack[-1]["content"].append(a)
                a = stack.pop()
                if(len(stack)==0):
                    original.append(a)
                    stack.append({"header": i.text, "content": []})
                else:
                    stack[-1]["content"].append(a)
                    stack.append({"header": i.text, "content": []})
        else:
            if(i.name == 'ul'):
                for index,j in enumerate(i.find_all('li')):
                    stack[-1]["content"].append(f"  {index+1}.{j.text}")
            if(i.name == 'ol'):
                for index,j in enumerate(i.find_all('li')):
                    stack[-1]["content"].append(f"  {index+1}.{j.text}")

            if(i.name == 'div'):
                code = i.find('code')
                if(code):
                    stack[-1]["content"].append({"code_example": code.text})
                else:
                    stack[-1]["content"].append(i.text)
          
            else:
                if(i.name == "ul" or i.name == "ol"):
                    continue
                else:
                    stack[-1]["content"].append(i.text)


    while(len(stack) > 1):
        a = stack.pop()
        stack[-1]["content"].append(a)
    original.append(stack.pop())

    return original


import json
from bs4 import BeautifulSoup
import requests

# Fetch the web page
url = "https://react.dev/learn/javascript-in-jsx-with-curly-braces"
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

soup = BeautifulSoup(response.text, 'html.parser')

# Locate the main content
outer_div = soup.find('main')
article = outer_div.find('article').find("div", class_="ps-0")
content = article.contents
h1 = content[0]
h1 = h1.find_all('h1')
h1 = h1[0].text
print(h1)
data = content[1]
data_footer = data.contents[1]
actual_data = data.contents[0]  
all_divs = actual_data.find_all('div', class_="max-w-4xl ms-0 2xl:mx-auto")
page_list = []
for index, div in enumerate(all_divs):
    page_list = page_list + div.contents
original = stack(page_list,h1)
output_file = "content_hierarchy.json"
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(original[0], file, ensure_ascii=False, indent=4)