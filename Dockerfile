FROM python:3.9-buster

WORKDIR /naisc-backend

RUN apt-get update && apt-get install -y \
  libgeos-dev \
  ffmpeg \
  libsm6 \
  libxext6 \
  libgl1-mesa-glx

RUN pip install -U peekingduck
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "python3", "main.py" ]
