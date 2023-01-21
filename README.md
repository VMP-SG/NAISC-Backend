# NAISC Backend

## To Run

1. Download Python at [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. Run the following lines of code
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
The server will be hosted at [http://127.0.0.1:5000](http://127.0.0.1:5000) by default.

## Deployment on AWS EC2

1. Create a systemd unit file
```sh
sudo nano /etc/systemd/system/helloworld.service
```

2. Add this into the file
```
[Unit]
Description=Gunicorn instance for hawk-eye centre backend
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/NAISC-Backend
ExecStart=/home/ubuntu/NAISC-Backend/.venv/bin/gunicorn -b 0.0.0.0:8080 main:app
Restart=always
[Install]
WantedBy=multi-user.target
```

3. Enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl start helloworld
sudo systemctl enable helloworld
```

4. Check that the service is running

```bash
curl localhost:8080
```

5. Stop the service

```bash
sudo systemctl daemon-reload
sudo systemctl stop helloworld
sudo systemctl disable helloworld
```
