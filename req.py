import requests
r = requests.get("https://api.github.com/search/repositories?q=language:python")
repo = r.json()
for i in repo["items"]:
    print(f"{i['forks']}, {i['name']}: {i['description']}")