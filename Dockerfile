FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP=src
ENV FLASK_ENV=development
EXPOSE 5000
CMD [ "/usr/local/bin/flask", "run",  "--host",  "0.0.0.0", "--port", "5000" ]