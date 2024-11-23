l = ['h1', 'h2', '1','2', 'h3', '3', 'h3', '4', 'h4', '5', 'h2', '6', 'h1', '7']

stack = [] 
original = []
for i in l:
    if(i in ['h1', 'h2', 'h3', 'h4']):
        level = int(i[1])
        current_stack_length = len(stack)
        if(current_stack_length < level):
            stack.append({"header": i, "content": []})
        elif(current_stack_length == level and current_stack_length != 0):
            a = stack.pop()
            stack[-1]["content"].append(a)
            stack.append({"header": i, "content": []})
        
        else:
            while(len(stack) > level):
                a = stack.pop()
                stack[-1]["content"].append(a)
            a = stack.pop()
            if(len(stack)==0):
                original.append(a)
                stack.append({"header": i, "content": []})
            else:
                stack[-1]["content"].append(a)
                stack.append({"header": i, "content": []})
    else:
        stack[-1]["content"].append(i)

print(original)