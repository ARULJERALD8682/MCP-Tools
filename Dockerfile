FROM python:latest

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 5051

CMD ["python", "bq_tools.py"]