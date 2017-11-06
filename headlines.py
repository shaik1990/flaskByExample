import feedparser
import requests
import urllib
import datetime
from flask import make_response
from flask import Flask, render_template, request
from forex_python.converter import CurrencyRates

app = Flask(__name__)

url = r"http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }

DEFAULTS = {'publication': 'bbc', 'city': 'London,UK',
            'currency_from': 'GBP',
            'currency_to': 'USD'
            }


@app.route("/")
def home():
    ''' Get a customised headlines, based on user input or defualt'''
    publication = get_value_with_fallback('publication')
    articles = get_news(publication)

    city = get_value_with_fallback('city')
    weather = get_weather(city)

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")

    rate = get_rate(currency_from, currency_to)
    # return render_template('headlines.html', articles=articles, weather=weather,
    #                        currency_from=currency_from, currency_to=currency_to,
    #                        rate=rate)
    response = make_response(render_template('headlines.html', articles=articles, weather=weather,
                                             currency_from=currency_from, currency_to=currency_to,
                                             rate=rate))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('publication', 'publication', expires=expires)
    response.set_cookie('city', city, expires=expires)
    response.set_cookie('currency_from', currency_from, expires=expires)
    response.set_cookie('currency_to', currency_to, expires=expires)
    return response

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()

    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    weather_url = r'http://api.openweathermap.org/data/2.5/weather?q={}&appid=3517b3c3ade621769fdfc02e9609b398'
    query = urllib.quote(query)
    url = weather_url.format(query)
    data = requests.get(url)
    parsed_data = data.json()
    weather = None
    if parsed_data['weather']:
        weather = {"description": parsed_data["weather"][0]["description"],
                   "temperature": parsed_data["main"]["temp"],
                   "city": parsed_data["name"],
                   "country": parsed_data['sys']['country']
                   }
    return weather


def get_rate(frm, to):
    c = CurrencyRates()
    return c.get_rate(frm, to)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
