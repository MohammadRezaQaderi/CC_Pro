FROM python:3.8-alpine

WORKDIR /app
 app.py requirements.txt /app

RUN pip install -r requirements.txt
CMD ["python", "app.py"]
