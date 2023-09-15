cd /home/wym
mkdir -p rrat
cd ./rrat
mkdir -p db
cd ./db
wget -nc https://github.com/YLashko/notes/raw/main/db.sqlite3
sudo chown $(whoami):$(whoami) ./db.sqlite3
cd ../
echo 'version: "3.7"
services:
  rrat:
    image: wymm/rrat-thesis:0.3
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
    volumes:
      - /usr/local/rrat/db:/app/db
volumes:
  rrat:' > docker-compose.yml
sudo systemctl start docker
sudo nohup sudo docker-compose up
