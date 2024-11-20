from bs4 import BeautifulSoup
import requests

def collect_content(tag):
    """
    Recursively collect the content from a tag, including its nested elements.
    """
    content = []
    
    # If the tag has text, add it to content
    if tag.string:
        content.append(tag.string.strip())
    
    # Now handle all child elements, e.g., nested tags
    for child in tag.children:
        if isinstance(child, str):  # Direct text node
            continue
        elif child.name in ['code', 'pre', 'p', 'ul', 'ol']:  # Handle specific tags
            content.append(collect_content(child))  # Recursively collect content
        else:
            content.append(child.get_text(strip=True))  # For other tags, just get text
    
    return content

def get_hierarchy(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming your main structure starts with the first <h1> or other tags
    headers = soup.find_all(['h1', 'h2', 'h3', 'h4'])

    result = []
    stack = []

    for header in headers:
        tag_level = int(header.name[1])  # Extract the level of the header (h1 = 1, h2 = 2, etc.)
        header_content = {"header": header.get_text(strip=True)}

        # Collect content between this header and the next one, handling nested elements
        siblings = []
        for sibling in header.find_next_siblings():
            if sibling.name in ['h1', 'h2', 'h3', 'h4'] and int(sibling.name[1]) <= tag_level:
                break  # Stop at the next header of the same or higher level
            
            # Collect sibling content (including nested elements)
            siblings.append(collect_content(sibling))
        
        # Add the collected sibling content to the header's content
        header_content["content"] = siblings
        
        # Now handle hierarchy with the stack
        while stack and stack[-1]["level"] >= tag_level:
            stack.pop()  # Pop elements that are of the same or higher level

        # Append to the correct level in the hierarchy
        if stack:
            stack[-1]["content"].append(header_content)
        else:
            result.append(header_content)

        # Push current header onto the stack with its level
        stack.append({"level": tag_level, "content": [header_content]})

    return result


# Example usage
url = 'https://react.dev/learn/tutorial-tic-tac-toe'  # Replace with the actual URL
hierarchy = get_hierarchy(url)
print(hierarchy)
