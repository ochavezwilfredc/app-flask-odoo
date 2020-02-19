FROM python:3.6
ADD . /app
WORKDIR /app
ADD ./app/requirements.txt .
RUN pip3 install -r /app/requirements.txt
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]