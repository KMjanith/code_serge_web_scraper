import requests

res = requests.get("https://docs.aws.amazon.com/lambda/latest/dg/toc-contents.json")

# Extract the section names
target_sections = [
    "What is AWS Lambda?",
    "Example apps",
    "Building with TypeScript",
    "Integrating other services",
    "Code examples"
]

contents = []
# Extract the URLs of the sections
for i in res.json()["contents"]:
    if i["title"] in target_sections:
        i["href"] = f"https://docs.aws.amazon.com/lambda/latest/dg/{i['href']}"
        # Check if "contents" key exists
        if i.get("contents"):
            for j in i["contents"]:
                j["href"] = f"https://docs.aws.amazon.com/lambda/latest/dg/{j['href']}"
        contents.append(i)
print(contents)  # Print the URLs of the target sections
