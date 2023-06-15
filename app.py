from fastapi import FastAPI
from transformers import pipeline
from dotenv import load_dotenv
import pydantic
import os
import torch
import uvicorn
import snscrape.modules.twitter as snstwitter
from pydantic import BaseModel
import re
from bs4 import BeautifulSoup
import requests
import json


load_dotenv()

app = FastAPI()

'''
content: css-1dbjc4n r-1s2bzr4
text: css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0
comment: css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0
'''

class TweetURL(pydantic.BaseModel):
    url: pydantic.HttpUrl


class Text(pydantic.BaseModel):
    text: str


@app.get('/')
def home():
    return ({
        "Project": "Cyberbullying detection",
        "Made By": {
            "1DS19IS076": "RAKSHITHA K",
            "1DS19IS068": "POOJA M",
            "1DS19IS108": "SREENIKETH MADGULA"
        }
    })


classifier = pipeline("sentiment-analysis",
                      model=os.getenv('MODEL_NAME'), top_k=None)


@app.post('/classify/text/')
def classify_text(text: Text):
    return {
        "content": text.text,
        "result": classifier(text.text)
    }

# def get_tweet_content(url):
#     html_text = requests.get(url).text
#     print(html_text)
#     soup = BeautifulSoup(html_text,'lxml')
#     content_body = soup.find('div', class_ = "css-1dbjc4n r-1s2bzr4")
#     print(content_body)

@app.post('/classify/link/')
def classify_link(obj: TweetURL):
    content = scrape_tweet(obj=obj)
    return {
        "content": content,
        "result": classifier(content)
    }

def scrape_tweet(obj: TweetURL):
    path = obj.url.path
    x = re.search(r"\/(\d+)$",path)
    # print(path)
    # print(x.groups())
    scraper = snstwitter.TwitterTweetScraper(tweetId=x.groups()[0])
    for i,item in enumerate(scraper.get_items()):
        data = json.loads(item.json())
        # print(type(data))
        return data["content"]
        # return item.json()["content"]
    # html_text = requests.get(url).text
    # soup = BeautifulSoup(html_text,'lxml')
    # url = obj.url
    # print(url)
    # get_tweet_content(url)


if __name__ == '__main__':
    uvicorn.run("app:app", port=8000, reload=False)