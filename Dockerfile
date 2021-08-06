FROM python:3.8
ENV PYTHONUNBUFFERED 1
ADD ovpn_spammer /
ADD requirements.txt /
RUN pip install -r requirements.txt