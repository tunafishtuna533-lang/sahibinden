import os, requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date

def get_listings():
    url = "https://www.hepsiemlak.com/tekirdag-satilik-arsa"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=20)
    
    listings = []
    lines = r.text.split('\n')
    
    for i, line in enumerate(lines):
        if 'ilan-basligi' in line or 'listing-title' in line or '"title"' in line:
            listings.append(line.strip()[:200])
        if len(listings) >= 10:
            break
    
    return listings, url

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = os.environ["SENDER_EMAIL"]
    msg["To"] = "mrc.tuna@hotmail.com"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.login(os.environ["SENDER_EMAIL"], os.environ["SENDER_PASSWORD"])
        s.send_message(msg)

def main():
    today = date.today().strftime("%d %B %Y")
    listings, url = get_listings()
    
    subject = "Tekirdag Satilik Arsa - " + today
    body = "Gunaydin!\n\n"
    body += "Tekirdag satilik arsa - " + today + "\n"
    body += "Kaynak: " + url + "\n"
    body += "=" * 40 + "\n\n"
    
    if not listings:
        body += "Bugun ilan verisi alinamadi. Siteyi manuel kontrol edin:\n" + url
    else:
        body += "Son ilanlardan veri:\n\n"
        for i, item in enumerate(listings, 1):
            body += str(i) + ". " + item + "\n\n"
    
    body += "\n---\nBu mail otomatik olarak gonderilmistir."
    send_email(subject, body)

if __name__ == "__main__":
    main()
