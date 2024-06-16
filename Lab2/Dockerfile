FROM python
RUN apt-get update && apt-get install -y iputils-ping

WORKDIR /usr/src/script

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-u", "main.py"]
