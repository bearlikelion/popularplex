FROM python:slim

COPY . /opt/popularplex

WORKDIR /opt/popularplex

RUN pip install -r requirements.txt

CMD ["python", "popular_plex.py"]