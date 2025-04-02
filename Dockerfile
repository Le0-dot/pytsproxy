FROM python:3.13.2-alpine3.21

COPY . /app

RUN pip install /app

ENTRYPOINT ["pytsproxy"]
CMD ["-p", "80"]
