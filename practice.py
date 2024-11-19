import requests
from bs4 import BeautifulSoup

def find_outer_topis(soup):
    aside = soup.find("aside")
    nav = aside.find("nav")
    all_li = nav.find_all("li")
    outer_li = [li for li in all_li if li.find("ul")]
    result = []
    for i in outer_li:
        result.append(i.find("a").find("div").text)
    print(result)
    return result

# URL of the React documentation page
url = "https://react.dev/learn"

# Send a GET request to fetch the webpage content
response = requests.get(url)
response.raise_for_status()  # Ensure the request was successful

# Parse the HTML content
soup = BeautifulSoup(response.text, 'html.parser')

find_outer_topis(soup)

# Find all <aside> elements
asides = soup.find_all("aside")

# Ensure <aside> exists
if asides:
    aside = asides[0]  # Select the first <aside>
    
    # Find all <ul> inside <aside>
    ul_elements = aside.find_all("ul")
    print(f"Total <ul> elements found: {len(ul_elements)}")

    # Process the outermost <ul> (first <ul>)
    if ul_elements:
        for i, outer_li in enumerate(ul_elements[0].find_all("li"), start=1):  # Iterate over <li> in the first <ul>
            #Safely get the <a> and <div> inside each <li>
            a_tag = outer_li.find("a")
            if a_tag:
                topic_div = a_tag.find("div")
                if topic_div:
                    topic_text = topic_div.text.strip()
                    topic_link = a_tag.get("href", "#")  # Get link or default to "#"
                    print(f"Outer Topic {i}: {topic_text} (Link: {topic_link})")
            
            #Optional: Check for nested <ul> and process inner <li>
            nested_ul = outer_li.find("ul")
            if nested_ul:
                print(f"  Inner topics for Outer Topic {i}:")
                for j, inner_li in enumerate(nested_ul.find_all("li"), start=1):
                    inner_a_tag = inner_li.find("a")
                    if inner_a_tag:
                        inner_topic = inner_a_tag.text.strip()
                        inner_link = inner_a_tag.get("href", "#")
                        print(f"    Inner Topic {j}: {inner_topic} (Link: {inner_link})")

                print("\n")
else:
    print("No <aside> elements found!")
