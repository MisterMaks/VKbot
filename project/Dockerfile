FROM python:3.7

COPY . /bot

WORKDIR /bot

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["bot.py"]
