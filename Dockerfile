FROM python:alpine
WORKDIR /app/
COPY requirements.txt   .
RUN pip install -r requirements.txt
COPY .           .
CMD gunicorn --bind 0.0.0.0:4001 run:hetch_translator
EXPOSE 4001
HEALTHCHECK CMD curl --fail http://0.0.0.0:4001/translator/all || exit 1