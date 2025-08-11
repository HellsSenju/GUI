apt install python3.12-venv

python3 -m venv .venv

source .venv/bin/activate



###
sudo apt install libpq-dev python3-dev build-essential



### конвертация  файла .ui в файл .py
pyuic5 main.ui -o mainwindow.py

pyuic5 custom_list_item.ui -o custom_list_item.py

### войти в консоль psql:
sudo -u postgres psql


# изменить пароль для postgres
\password postgres



### уставновка монго:
# Import the public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create list file (choose the appropriate one for your Ubuntu version)
# For Ubuntu 22.04 (Jammy):
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# For Ubuntu 20.04 (Focal):
# echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# For Ubuntu 18.04 (Bionic):
# echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

sudo apt update
sudo apt install mongodb-org


# Запуск MongoDB
sudo systemctl start mongod

# Подключиться к MongoDB
mongosh

