# coding:utf8
import requests
import lxml.html
import flask
import time
import json
from flask import request, jsonify
from lxml.etree import tostring
from markdownify import markdownify as md

EKSI_BASE_URL = "http://eksisozluk.com"
POPULAR_TOPICS_URL = EKSI_BASE_URL + "/basliklar/gundem?p="
EKSI_CHANNELS_URL = EKSI_BASE_URL + "/kanallar"
EKSI_AUTOCOMPLETE_URL = EKSI_BASE_URL + "/autocomplete/query?q="
EKSI_PAGE_PARAMETER = "?p="


def generateTopicPageUrl(path, page):
    return EKSI_BASE_URL + path + EKSI_PAGE_PARAMETER + page


class Topic:
    def __init__(self, title, numberOfComments, url):
        self.title = title
        self.numberOfComments = numberOfComments
        self.url = url

    # might need to converto https
    def serialize(self):
        return {
            'title': self.title.strip(),
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


class Channel:
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def serialize(self):
        return {
            'title': self.title,
            'url': self.url
        }


class AutoComplete:
    def __init__(self, title):
        self.title = title

    def serialize(self):
        return {
            'title': self.title
        }


app = flask.Flask(__name__)
app.config["DEBUG"] = True


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}


def autoComplete(query):
    customHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}
    response = requests.get(EKSI_AUTOCOMPLETE_URL + query + "&_=" +
                            str(int(round(time.time() * 1000))), headers=customHeaders)
    responseValue = json.loads(response.text)
    value = responseValue["Titles"]
    results = AutoComplete(value)
    return results


def getTopics(url):
    topicList = []

    response = requests.get(url, headers=headers)
    tree = lxml.html.fromstring(response.text)
    ulTag = tree.cssselect("[class=topic-list]")[0]
    for liTag in ulTag.cssselect("a"):
        smallTag = liTag.cssselect("small")
        topicTitle = liTag.text
        if smallTag:
            numberOfComments = smallTag[0].text_content()
        else:
            numberOfComments = "0"
        topicUrl = liTag.get("href")
        popularTopic = Topic(topicTitle, numberOfComments, topicUrl)
        topicList.append(popularTopic)
    return topicList


def getComments(url):
    commentList = []

    response = requests.get(url, headers=headers)
    tree = lxml.html.fromstring(response.text)
    ulTag = tree.cssselect("[id=entry-item-list]")[0]

    contentList = []
    authorList = []
    dateList = []

    tree.cssselect('[class="pager"]')[0].get('data-pagecount')

    for content in ulTag.cssselect('[class="content"]'):
        contentAsHTMLString = tostring(content).decode("utf-8")
        contentList.append(md(contentAsHTMLString).strip())

    for author in ulTag.cssselect("[class=entry-author]"):
        authorUrl = author.get("href")
        authorList.append((authorUrl, author.text_content()))

    for date in ulTag.cssselect("a.entry-date.permalink"):
        dateList.append((date.text_content(), date.get("href")))

    for index, element in enumerate(contentList):
        content = contentList[index]
        authorUrl = authorList[index][0]
        author = authorList[index][1]
        date = dateList[index][0]
        commentUrl = dateList[index][1]

        comment = Comment(content, date, author, authorUrl, commentUrl)
        commentList.append(comment)

    return commentList


def getChannels():
    response = requests.get(EKSI_CHANNELS_URL, headers=headers)
    tree = lxml.html.fromstring(response.text)
    ulTag = tree.cssselect("[id=channel-follow-list]")
    channelList = []
    channel = ulTag[0].cssselect("[class=index-link]")
    for item in channel:
        channelList.append(
            Channel(item.text_content(), item.get("href")))

    return channelList


@app.route('/api/v1/channels', methods=['GET'])
def api_getChannels():
    channelList = getChannels()
    return jsonify(
        channels=[e.serialize() for e in channelList]
    )


@app.route('/api/v1/topics', methods=['GET'])
def api_getTopics():
    args = request.args
    urlPath = args["path"]
    page = args['page']
    popularList = getTopics(
        generateTopicPageUrl(path=urlPath, page=page))
    return jsonify(
        popularTopics=[e.serialize() for e in popularList]
    )


@app.route('/api/v1/popular', methods=['GET'])
def api_getPopularTopics():
    args = request.args
    page = args['page']
    popularList = getTopics(
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


@app.route('/api/v1/search', methods=['GET'])
def api_search():
    args = request.args
    query = args['query']
    results = autoComplete(query)
    return jsonify(
        comments=[results.serialize()]
    )


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run()
