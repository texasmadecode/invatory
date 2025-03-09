FROM ubuntu:18.04
RUN apt-get update

WORKDIR /app
COPY app/ /app
COPY app/templates/ /app/templates
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

CMD python app.py