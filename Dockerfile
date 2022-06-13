FROM python:3.9.13

WORKDIR /open-etl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_APP=run.py

CMD [ "./docker/init.sh"]
