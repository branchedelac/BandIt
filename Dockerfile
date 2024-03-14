FROM python:3.10-bookworm

COPY requirements_prod.txt /requirements_prod.txt
COPY setup.py setup.py
COPY Makefile Makefile

RUN apt-get update
RUN apt-get install -y fluidsynth
RUN pip install --upgrade pip
RUN pip install -r requirements_prod.txt

COPY backend backend
RUN pip install .

CMD uvicorn backend.api.app:app --host 0.0.0.0 --port $PORT
