FROM python:3.10

WORKDIR ./

COPY requirements.txt ./

RUN pip install --upgrade -r requirements.txt

COPY . .

CMD ["python", "app.py"]