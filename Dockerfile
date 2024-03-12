FROM python:3.10.13-slim-bullseye

WORKDIR .
COPY . .

RUN pip3 install -r  requirements.txt

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:80"]

EXPOSE 80
