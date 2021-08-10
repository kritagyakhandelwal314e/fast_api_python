FROM python


RUN mkdir /app
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -U -r requirements.txt

COPY ./ ./

CMD ["uvicorn", "main:app", "--reload"]