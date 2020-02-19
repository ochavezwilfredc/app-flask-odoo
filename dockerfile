FROM python:3.6
COPY ./app /app
WORKDIR /app
RUN pip install flask Flask-Cors OdooRPC gunicorn
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]

# docker build --tag flask_gunicorn_app .
# docker run --detach -p 80:8000 flask_gunicorn_app
