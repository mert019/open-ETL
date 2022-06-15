FROM python:3.9.13

WORKDIR /open-etl

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
# Convert line CRLF to LF.
RUN sed -i -e 's/\r$//' ./docker/init.sh

EXPOSE 8080

ENV FLASK_APP=run.py

RUN chmod +x ./docker/init.sh
CMD [ "./docker/init.sh"]