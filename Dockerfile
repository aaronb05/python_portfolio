FROM python:3.10

COPY requirements.txt /tmp/

WORKDIR /python_portfolio

RUN pip install -r /tmp/requirements.txt

COPY . /python_portfolio

ENTRYPOINT ["python"]

EXPOSE 5000

CMD ["server.py"]
