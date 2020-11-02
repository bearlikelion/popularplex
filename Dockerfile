FROM python:3

ADD popular_plex.py /usr/src/popularplex

COPY requirements.txt /usr/src/popularplex

COPY config.ini /usr/src/popularplex

WORKDIR /usr/src/popularplex

RUN pip install -r requirements.txt

CMD ["python", "popular_plex.py"]