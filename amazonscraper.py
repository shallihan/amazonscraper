import requests
from bs4 import BeautifulSoup
import smtplib
from decouple import config

URL = config('PRODUCT_URL')

headers = {"User-Agent": config('USER_AGENT')}

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(config('LOGIN_EMAIL'), config('LOGIN_PASSWORD'))

    subject = 'Amazon Price Scraper: The price has fallen'
    body = "Quickly, check it out yourself. " + URL

    msg = f"Subject: {subject}\n\n{body.encode('utf-8')}"

    server.sendmail(
        config('SENDER'),
        config('RECIEVER'),
        msg
    )
    print("Email sent to you 📬")
    server.quit()

def check_price():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find(id='productTitle').get_text()
    print(title.strip())
    price = soup.find(id='priceblock_ourprice').get_text()
    converted_price = float(price[1:6])
    if(converted_price <= 1000):
        send_mail()
    print(price)


check_price()