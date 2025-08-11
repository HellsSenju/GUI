 
`apt install python3.12-venv` - в этой команде может менятся версия после 3. 

`python3 -m venv .venv` - если не будет нужного python3.12-venv, то после выполнения этой команды будет подсказка, что установить

source .venv/bin/activate



### надо для некоторых пакетов питона
sudo apt install libpq-dev python3-dev build-essential



### конвертация  файла .ui в файл .py
pyuic5 main.ui -o mainwindow.py

pyuic5 custom_list_item.ui -o custom_list_item.py

### войти в консоль psql:
sudo -u postgres psql


# изменить пароль для postgres
\password postgres



# уставновка монго UBUNTU: 
### Import the public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

### Create list file (choose the appropriate one for your Ubuntu version)
### For Ubuntu 22.04 (Jammy):
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

### For Ubuntu 20.04 (Focal):
### echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

### For Ubuntu 18.04 (Bionic):
### echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install mongodb-org


### Запуск MongoDB
sudo systemctl start mongod

### Подключиться к MongoDB
mongosh



# уставновка монго DEBIAN (не работает):
sudo apt install -y curl
### Импортировать публичный ключ GPG MongoDB:
curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
### Добавить репозиторий MongoDB:
echo "deb [signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg] https://repo.mongodb.org/apt/debian buster/mongodb-org/6.0 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
### Обновить список пакетов и установить MongoDB:
sudo apt update
sudo apt install -y mongodb-org


# уставновка монго Docker:
sudo apt install -y docker.io
sudo systemctl start docker

sudo docker run -d -p 27017:27017 --name mongodb mongo:6.0

sudo docker exec -it mongodb mongosh --eval "db.runCommand({ping: 1})"


# Portainer

### Создайте volume для хранения данных
sudo docker volume create portainer_data

### Запустите Portainer
sudo docker run -d \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest


### Откройте в браузере:
https://localhost:9443



