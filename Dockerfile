FROM python:3.8-slim-buster
RUN apt update -y && apt upgrade -y && \ 
    apt install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* 
RUN git clone https://github.com/Rajbhaiya/file-sharing/ /app
WORKDIR /app
RUN pip3 install -r requirements.txt

CMD ["bash", "start"]
