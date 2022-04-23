FROM python:3.7.2-stretch

# Add non root user
WORKDIR /app/
COPY requirements.txt   .

ENV PATH=$PATH:/app/.local/bin:/app/python/bin/
ENV PYTHONPATH=$PYTHONPATH:/app/python

RUN pip install -r requirements.txt --target=/app/python

# COPY ALL THE REST OF THE SOURCE CODE
COPY .           .

WORKDIR /app/

# SETUP FLASK APP TO RUN
WORKDIR /app/

# ENV FLASK_ENV=prod
# ENV FLASK_APP=server:currency_converter

CMD ["uwsgi", "app.ini"]

# HEALTHCHECK --interval=3s CMD [ -e /tmp/.lock ] || exit 1