import smtplib
from config import EMAIL,EMAIL_PASSWORD

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

print("EMAIL:", EMAIL)
print("EMAIL_PASSWORD LENGTH:", len(EMAIL_PASSWORD))

server.login(EMAIL, EMAIL_PASSWORD)

print("LOGIN SUCCESS")
server.quit()