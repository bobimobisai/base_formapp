FROM python:3.10.13-slim-bullseye

WORKDIR .
COPY . .

RUN pip3 install -r  requirements.txt

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:443", "--certfile", "src/ssl/certificate.crt", "--keyfile", "src/ssl/private.key"]

EXPOSE 443
