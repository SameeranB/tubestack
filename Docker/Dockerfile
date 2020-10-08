FROM python:3.8.5-alpine 

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev zlib-dev jpeg-dev

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD python Docker/wait_for_db.py && \
    python manage.py migrate && \
    python manage.py initadmin && \
    python manage.py runserver 0.0.0.0:8000


EXPOSE 8000