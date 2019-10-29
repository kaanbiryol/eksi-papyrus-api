# eksi-papyrus-api
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/kaanbiryol/eksi-papyrus-api)

Python API for [Papyrus for Eksi](https://github.com/kaanbiryol/eksi-papyrus-flutter), a clean eksi-sozluk reading app for mobile.

Run it locally or deploy it to Heroku to test it with the [Papyrus for Eksi](https://github.com/kaanbiryol/eksi-papyrus-flutter).

## Routes

* Get comments of specific topic

  ```/api/v1/comments?url=EKSI_SOZLUK_TOPIC_URL&type=COMMENTS_TYPE&page=PAGE_NO```

* Get search results for query
  
  ```/api/v1/search?query=YOUR_SEARCH_QUERY```

*  Get topics for specific channel
  
    ```/api/v1/topics?path=CHANNEL_PATH&page=PAGE_NO```

* Get channels

  ```api/v1/channels```

* Get topic URL for a specific query text

  ```api/v1/query?q=QUERY_TEXT```
  
* Avaliable COMMENT_TYPE's;
  
  ```
  today = 0
  popular = 1
  all = 2
  ```
  
```
MIT License

Copyright (c) 2019 Kaan Biryol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
