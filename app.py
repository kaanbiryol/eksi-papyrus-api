import requests
import lxml.html
import flask
from flask import request, jsonify


class PopularTopics:
    def __init__(self, title, numberOfComments, url):
        self.title = title
        self.numberOfComments = numberOfComments
        self.url = url

    def serialize(self):
        return {
            'title': self.title,
            'numberOfComments': self.numberOfComments,
            'url': self.url
        }


app = flask.Flask(__name__)
app.config["DEBUG"] = True

url = 'http://eksisozluk.com/basliklar/gundem?p=1'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}

popularList = []

response = requests.get(url, headers=headers)
tree = lxml.html.fromstring(response.text)
ulTag = tree.cssselect("[class=topic-list]")[0]
for liTag in ulTag.cssselect("a"):
    smallTag = liTag.cssselect("small")
    title = liTag.text
    numberOfComments = smallTag[0].text_content()
    url = liTag.get("href")
    print(title, numberOfComments)
    gundemObj = PopularTopics(title, numberOfComments, url)
    popularList.append(gundemObj)


@app.route('/api/v1/popular', methods=['GET'])
def api_all():
    return jsonify(
        popularTopics=[e.serialize() for e in popularList]
    )


if __name__ == '__main__':
    app.run()
