FROM python:3.10.16-bookworm

ADD app.py .
ADD requirements.txt .

RUN pip install -r requirements.txt
RUN apt update && apt install postgresql-client -y

CMD ["python3" "app.py"]