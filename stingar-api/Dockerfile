FROM jfloff/alpine-python

RUN pip install elasticsearch elasticsearch-dsl falcon requests gunicorn

COPY api /api
WORKDIR /api

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "app"]
