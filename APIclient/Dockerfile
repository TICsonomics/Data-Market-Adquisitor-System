FROM python:latest
WORKDIR /code
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY APIclient.py APIclient.py
CMD ["python", "-u", "APIclient.py"]
