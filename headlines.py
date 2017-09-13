import feedparser

from flask import Flask, render_template

app = Flask(__name__)

url = r"http://feeds.bbci.co.uk/news/rss.xml"
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'
             }


@app.route('/')
@app.route('/<publication>')
def get_news(publication="bbc"):
    feed = feedparser.parse(RSS_FEEDS[publication])
    feed_article = feed['entries'][0]
    articles = feed['entries']
    return render_template("headlines.html", articles=articles, channel=publication)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
