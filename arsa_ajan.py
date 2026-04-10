import os, requests, smtplib, re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

def get_listings():
    url = "https://www.emlakjet.com/satilik-arsa/tekirdag/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=20)
    
    listings = []
    
    titles = re.findall(r'"title"\s*:\s*"([^"]{10,100})"', r.text)
    prices = re.findall(r'"price"\s*:\s*"?(\d[\d\.,]+)"?', r.text)
    
    for i in range(min(10, len(titles))):
        price = prices[i] if i < len(prices) else "-"
