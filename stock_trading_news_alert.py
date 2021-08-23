import os
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


news_api_key = os.getenv("NEWS_API_KEY")
alphavantage_api_key = os.getenv("ALPHAVANTAGE_API_KEY")

company_name = "GOOGL"
alphavantage_url = "https://www.alphavantage.co/query"
alphavantage_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": company_name,
    "apikey": alphavantage_api_key
}

news_url = "https://newsapi.org/v2/everything"
news_parameters = {
    "qInTitle": company_name,
    "apiKey": news_api_key
}
email = os.getenv("GOOGLE_TEST_EMAIL")
password = os.getenv("GOOGLE_TEST_EMAIL_PASSWORD")


def send_email(email, password, emails, subject, message, smtp="smtp.gmail.com"):
    msg = MIMEMultipart()

    msg["From"] = email
    msg["To"] = emails
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html", "utf-8"))

    with smtplib.SMTP(smtp) as connection:
        connection.starttls()
        connection.login(email, password)
        connection.sendmail(
            from_addr=msg["From"],
            to_addrs=msg["To"],
            msg=msg.as_string())


response = requests.get(alphavantage_url, params=alphavantage_parameters)
response.raise_for_status()
data = response.json()

data_as_list = [trade_value for (trade_key, trade_value) in data["Time Series (Daily)"].items()]
last_value = float(data_as_list[0]["4. close"])
before_last_value = float(data_as_list[1]["4. close"])
difference = last_value - before_last_value
diff_percent = (abs(difference) / last_value) * 100

if diff_percent >= 1:
    print(f"last: {last_value}\nbefore: {before_last_value}\ndifference: {difference}\npercentage: {diff_percent}%")
    response = requests.get(news_url, params=news_parameters)
    response.raise_for_status()
    data = response.json()["articles"][:5]
    text = ""
    for article in data:
        text += f""" <h2> {article['title']}</h2><br/><br/>
                     <p><h3>{article['description']}</h3>
                     <a href='{article['url']}'>Go to the link</a></p><br/><br/>
                """
    send_email(
        email,
        password,
        email,
        "Stock Trading Alert",
        text
        )



