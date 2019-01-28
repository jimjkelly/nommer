FROM python:3.7-slim

WORKDIR /app

ENV PYTHONPATH /app/src
ENV FLASK_APP nommer

# Add the wait script to the image - this allows us to ensure dependencies
# are available when the container starts. 
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.5.0/wait /usr/local/bin/wait
RUN chmod +x /usr/local/bin/wait

RUN pip install poetry
RUN poetry config settings.virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . /app

CMD wait && gunicorn -w 4 -b 0.0.0.0:80 nommer:app
