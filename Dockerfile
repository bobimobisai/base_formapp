FROM python:3.10


WORKDIR .
COPY . .


RUN pip3 install --upgrade setuptools
RUN pip3 install -r  requirements.txt

CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "-b", "0.0.0.0:8000"]

EXPOSE 8000
