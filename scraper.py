import requests
from bs4 import BeautifulSoup
import smtplib
import datetime
import time

URL = 'UrlOfAuction'

my_email = 'test@gmail.com'

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}


def check_time():
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find(id='itemTitle').get_text().strip('Details about').strip()
    time_left = soup.find(id='vi-cdown_timeLeft').get_text().strip()
    current_price = soup.find(
        id='prcIsum_bidPrice').get_text().strip('US').strip()

    h, m, s = time_left.split(' ')
    h = h.strip('h')
    m = m.strip('m')
    s = s.strip('s')
    time_left_in_seconds = int(datetime.timedelta(
        hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
    if time_left_in_seconds > 300:
        time.sleep(1)
        check_time()
    send_mail()


def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('ebayauctionscraper@gmail.com', 'ebayauctionscraperpassword1')

    subject = 'Time is running out!'
    body = f'There is only 5 more minutes left on one of your interested auctions. Click this link to go bid! {URL}'

    msg = f'Subject: {subject}\n\n{body}'

    server.sendmail(
        'ebayauctionscraper@gmail.com',
        my_email,
        msg
    )

    server.quit()
    print('email sent')


check_time()
