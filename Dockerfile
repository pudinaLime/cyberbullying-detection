FROM python:3.10

WORKDIR ./

COPY requirements.txt ./

RUN pip install --upgrade pip; pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]