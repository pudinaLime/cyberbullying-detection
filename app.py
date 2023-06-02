from fastapi import FastAPI
from transformers import pipeline
from dotenv import load_dotenv
import pydantic
import os
import torch
import uvicorn

load_dotenv()

app = FastAPI()


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


@app.post('/classify')
def classify(text: Text):
    return classifier(text.text)


if __name__ == '__main__':
    uvicorn.run("app:app", port=8000, reload=True)