import re


class Utilities:
    def __init__(self):
        pass

    #function to remove ascii characters from the string
    def remove_ascii(self,text):
        return re.sub(r'[^\x00-\x7F]+', '', text)
    
    def return_data(self, stack, content_name):
        # poping and making the json hirachi and output the page data as a list of dictionaries
        original = []
        while(len(stack) > 1):
            a = stack.pop()
            stack[-1][content_name].append(a)
        original.append(stack.pop())
        return original
    
    # this function take a list of lists of tags and return a single list of tags
    def make_item_list(self, all_divs):
        page_list = []
        for index, div in enumerate(all_divs):
            #print(div.get('class'))
            if(div.get('class')[0] == 'sandpack'):
                page_list.append(div)
            else:
                page_list = page_list + div.contents

        return page_list
    
    # make the string replacing redundant strings
    def remove_redundant(self, string):
        replace_targets = ["\n", "index.js", "index.html", "index.css", "App.js", " ResetFork", "Show more"]

        # Replace using a loop
        processed_text = string
        for target in replace_targets:
            processed_text = processed_text.replace(target, '')
        return processed_text