# Hawk-Eye Centre

Hawk-Eye Centre is an **integrated data source** powered by Machine Learning capabilities. Using computer vision models and pipelines from the PeekingDuck library, Hawk-Eye Centre can process large volumes of relevant information like people, furniture and cutlery from video feeds. Interested parties may then utilise this data API to perform higher level analysis and service. 

## 🛠️ To Run

1. Download Python at [https://www.python.org/downloads/](https://www.python.org/downloads/)

### For Linux
2. Run the following lines of code
```bash
sudo apt-get install ffmpeg libsm6 libxext6 libgeos-dev -y
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### For MacOS
2. Run the following lines of code
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

### For Windows
2. Run the following lines of code 
```bash
python -m venv .venv
.venv/Scripts/activate
pip install -r requirements.txt
python main.py
```

The server will be hosted at [http://127.0.0.1:5000](http://127.0.0.1:5000) by default.

## 🎯 Endpoints

#### `GET /api`

Response Content-Type:
```
text/event-stream
```

Response (JSON):
```js
{
  "A": {
    "raw_frame": [[[168, 181, 192], [172, 184, 195], [176, 188, 202]]],
    "labelled_frame": [[[[172, 183, 194], [174, 186, 196], [178, 191, 201]]]],
    "total_people_count": 0,
    "zone_people_count": [3, 0, 1, 1, 2, 0, 2],
    "zone_mapping": [100, 101, 102, 103, 104, 105, 0]
  },
  "B": {...},
  "C": {...},
  "D": {...}
}
```

#### `GET /video/raw/<zone_id>`
URL Parameter(s):

`zone_id`: ID of the Hawker Centre Zone (eg. A)

Response Content-Type:
```
multipart/x-mixed-replace
```

Response:
```
Raw Live Camera Feed
```

#### `GET /video/filter/<zone_id>`
URL Parameter(s):

`zone_id`: ID of the Hawker Centre Zone (eg. A)

Response Content-Type:
```
multipart/x-mixed-replace
```

Response:
```
Live Camera Feed with Bounding Boxes
```

#### `GET /count/zones`

Response Content-Type:
```
text/event-stream
```

Response:
```js
{
  "E": 13, 
  "D": 4, 
  "A": 11, 
  "B": 7, 
  "C": 11
}
```

#### `GET /count/zone/<zone_id>`
URL Parameter(s):

`zone_id`: ID of the Hawker Centre Zone (eg. A)

Response Content-Type:
```
text/event-stream
```

Response:
```js
[3, 0, 1, 1, 2, 0, 2]
```

#### `GET /count/queues`

Response Content-Type:
```
text/event-stream
```

Response:
```js
{
  "2": 1, 
  "0": 1, 
  "1": 5
}
```

#### `GET /count/queue/<stall_id>`
URL Parameter(s):

`stall_id`: ID of the Hawker Centre Stall (eg. 0)

Response Content-Type:
```
text/event-stream
```

Response:
```js
0
```

#### `GET /occupancy/tables`
Response Content-Type:
```
text/event-stream
```

Response:
```js
{
  "140": false, 
  "141": false, 
  ...
  "122": true
}
```

#### `GET /count/tables`
Response Content-Type:
```
text/event-stream
```

Response:
```js
{
  "140": 0, 
  "141": 0, 
  ...
  "122": 2
}
```

#### `GET /count/table/<table_id>`
URL Parameter(s):
`table_id`: ID of the Hawker Centre Table (eg. 140)

Response Content-Type:
```
text/event-stream
```

Response:
```js
0
```
