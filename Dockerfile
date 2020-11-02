FROM python:3

ADD popular_plex.py /usr/src/popularplex

COPY requirements.txt /usr/src/popularplex

COPY config.ini /usr/src/popularplex

RUN pip install -r /usr/src/popularplex/requirements.txt

CMD ["python", "/usr/src/popularplex/popular_plex.py"]