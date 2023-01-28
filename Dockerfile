FROM tensorflow/tensorflow:2.7.4

WORKDIR /naisc-backend

RUN apt-get update && apt-get install -y \
  libgeos-dev \
  ffmpeg \
  libsm6 \
  libxext6

RUN pip install -U peekingduck
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD [ "python3", "main.py" ]
