FROM python:3.8-slim

RUN mkdir -p /usr/src
WORKDIR /usr/src
COPY ./requirements.txt /usr/src/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/

CMD python /usr/src/main.py
