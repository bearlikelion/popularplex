FROM python:3

ADD popular_plex.py /usr/src/popularplex

ADD requirements.txt /usr/src/popularplex

ADD config.ini /usr/src/popularplex

RUN pip install -r /usr/src/popularplex/requirements.txt

CMD ["python", "/usr/src/popularplex/popular_plex.py"]