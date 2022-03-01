import smtplib

import requests

server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()
server.ehlo()
server.login("petrustestausjee@gmail.com", "TosiSalainen1!")
msg = "\n Health check failed"

r = requests.get('http://40.114.211.125/health.html')
if r.status_code == 200:
    print("Jee")
    
else:
    print("voi paska")
    server.sendmail("petrustestausjee@gmail.com", "petrustestausjee@gmail.com", msg)