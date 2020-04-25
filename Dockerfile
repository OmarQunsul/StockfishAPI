FROM python:3.9.0a5-buster

RUN apt-get update --fix-missing -qq
RUN apt-get -y install python3-pip stockfish
RUN ["pip3", "install", "stockfish"]
RUN ["pip3", "install", "flask"]
ADD engine.py /

ENV FLASK_APP=engine.py
CMD ["flask", "run", "--host=0.0.0.0"]
