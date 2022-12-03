FROM ubuntu

RUN apt-get update && apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install requests

WORKDIR /app
COPY . .

ENV CONSOLE_USER=default
ENV CONSOLE_PASS=default

ENV CONSOLE_URL=default
ENV CUST_SIZE=default
ENV CUST_PAGE=default

CMD [ "python3", "./ivm_apiv3_endpoint_500_check.py" ]

#TODO - Reduce size