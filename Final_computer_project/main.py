# Using requests to be able to extract data from a website using its url
import requests
# BeautifulSoup to scrape website
from bs4 import BeautifulSoup

# smtplib to send an email
import smtplib

# time to periodically check price
import time

op_msg = "Hello! This is a program to track the price of your favorite amazon product.\nIt will periodically checks the price every hour, and will notify you vie email when the product is within your budget."
print(op_msg)

URL = input("Paste your amazon product's url here > ")
try:
    compare_price = float(input('Enter your budget: '))
except ValueError:
    print('Input should be a numeral.')
    quit()
email_id = input('Please enter your email-id > ')

# Information about browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
}

# returning all data from the website
page = requests.get(URL, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
# returning product title through id
title = soup.find(id='productTitle').get_text()
print(title.strip())


def price_check():
    # returning product price
    page_p = requests.get(URL, headers=headers)
    soup_p = BeautifulSoup(page_p.content, 'html.parser')
    converted_price = 0

    # Checking which id for product is present on webpage
    if soup_p.find(id='priceblock_ourprice') != None:
        price = soup_p.find(id='priceblock_ourprice').get_text()
        converted_price = float(price[2:].replace(',', ''))

    elif soup_p.find(id='priceblock_dealprice') != None:
        price = soup_p.find(id='priceblock_dealprice').get_text()
        converted_price = float(price[2:].replace(',', ''))

    elif soup_p.find(id='priceblock_saleprice') != None:
        price = soup_p.find(id='priceblock_saleprice').get_text()
        converted_price = float(price[2:].replace(',', ''))

    else:
        print("Sorry! we couldn't retrieve the price of this product, try another product.")
        quit()

    print('Price:', converted_price)

    if converted_price <= compare_price:
        print('Looks like the product is in your budget.')

        # Calling send_mail function to send an email if product price is within range
        send_mail()
        quit()
    else:
        print('Looks like the product is not in your budget, an emil will be sent when it fits your budget.')


def send_mail():
    # establishing connection between our and gmail
    # gmail connection number 587
    server = smtplib.SMTP('smtp.gmail.com', 587)

    # Extended simple mail transfer protocol
    server.ehlo()

    # server.starttls to encrypt our connection
    server.starttls()
    server.ehlo()

    # Login in to email with 2-step verified password
    server.login('akshatshrivastavab@gmail.com', 'pbgvrcaooujmdvxf')

    subject = 'Hey! looks like your amazon product is in your budget now.'
    body = f'Check the amazon link: {URL}'
    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail('akshatshrivastavab@gmail.com',
                    email_id,
                    msg,
                    )
    print('HEY! THE EMAIL HAS BEEN SENT.')

    server.quit()


while True:
    price_check()
    # time.sleep to run while loop every hour to call check_price
    time.sleep(60 * 60)