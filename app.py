# coding:utf8
import requests
import lxml.html
import flask
from flask import request, jsonify

EKSI_BASE_URL = "http://eksisozluk.com"
POPULAR_TOPICS_URL = "http://eksisozluk.com/basliklar/gundem?p="


class PopularTopic:
    def __init__(self, title, numberOfComments, url):
        self.title = title
        self.numberOfComments = numberOfComments
        self.url = url

    def serialize(self):
        return {
            'title': self.title,
            'numberOfComments': self.numberOfComments,
            'url': EKSI_BASE_URL + self.url.split('?')[0]
        }


class Comment:
    def __init__(self, comment, date, ownerUsername, ownerProfileUrl, commentUrl):
        self.comment = comment
        self.date = date
        self.ownerUsername = ownerUsername
        self.ownerProfileUrl = ownerProfileUrl
        self.commentUrl = commentUrl

    def serialize(self):
        return {
            'comment': self.comment,
            'date': self.date,
            'ownerUsername': self.ownerUsername,
            'ownerProfileUrl': EKSI_BASE_URL + self.ownerProfileUrl,
            'commentUrl': EKSI_BASE_URL + self.commentUrl
        }


app = flask.Flask(__name__)
app.config["DEBUG"] = True


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}


def getPopularTopics(url):
    popularList = []

    response = requests.get(url, headers=headers)
    tree = lxml.html.fromstring(response.text)
    ulTag = tree.cssselect("[class=topic-list]")[0]
    for liTag in ulTag.cssselect("a"):
        smallTag = liTag.cssselect("small")
        topicTitle = liTag.text
        numberOfComments = smallTag[0].text_content()
        topicUrl = liTag.get("href")
        popularTopic = PopularTopic(topicTitle, numberOfComments, topicUrl)
        popularList.append(popularTopic)
    return popularList


def getComments(url):
    commentList = []

    response = requests.get(url, headers=headers)
    tree = lxml.html.fromstring(response.text)
    ulTag = tree.cssselect("[id=entry-item-list]")[0]

    contentList = []
    authorList = []
    dateList = []

    for content in ulTag.cssselect('[class="content"]'):
        contentList.append(content.text_content())
        print(content.text_content())

    for author in ulTag.cssselect("[class=entry-author]"):
        authorUrl = author.get("href")
        authorList.append((authorUrl, author.text_content()))
        print(author.text_content(), authorUrl)

    for date in ulTag.cssselect("a.entry-date.permalink"):
        dateList.append((date.text_content(), date.get("href")))
        print(date.text_content(), date.get("href"))

    for index, element in enumerate(contentList):
        content = contentList[index]
        authorUrl = authorList[index][0]
        author = authorList[index][1]
        date = dateList[index][0]
        commentUrl = dateList[index][1]

        comment = Comment(content, date, author, authorUrl, commentUrl)
        commentList.append(comment)

    return commentList


@app.route('/api/v1/popular', methods=['GET'])
def api_getPopularTopics():
    args = request.args
    page = args['page']
    popularList = getPopularTopics(
        POPULAR_TOPICS_URL + page)
    return jsonify(
        popularTopics=[e.serialize() for e in popularList]
    )


@app.route('/api/v1/comments', methods=['GET'])
def api_getComments():
    args = request.args
    baseCommentUrl = args['url']
    page = args['page']
    commentList = getComments(
        baseCommentUrl + '?p=' + page)
    return jsonify(
        comments=[e.serialize() for e in commentList]
    )


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
