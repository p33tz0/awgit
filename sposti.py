import smtplib
server = smtplib.SMTP('smtp.gmail.com', 587)

server.ehlo()
server.starttls()
server.ehlo()

server.login("petrustestausjee@gmail.com", "TosiSalainen1!")

msg = "\n Tässä sähköpostia"
server.sendmail("petrustestausjee@gmail.com", "petrustestausjee@gmail.com", msg.encode("ascii", errors="ignore"))