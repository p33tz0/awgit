import requests
r = requests.get('http://40.114.211.125/health.html')
if r.status_code == 200:
    print("Jee")
else:
    print("voi paska")