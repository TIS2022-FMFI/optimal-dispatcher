# optimal-dispatcher
Application that collects data from delivery dispatchers and optimizes resources

## Project setup for developers
Clone repository.

Create virtual enviroment inside root folder of repository.
```
python -m venv venv
```
Activate virtual enviroment.
```
path\to\folder>venv\Scripts\actiate.bat
```
Install necessary libraries inside virtual enviroment.
```
(venv)>pip install -r requirements.txt
```
Create .env file inside config file.

Structure of .env file
```
DB_NAME="database_name"
DB_USER="database_user_name"
DB_PASSWORD="database_user_password"
PORT=DB_port(default 5432)
HOST="127.0.0.1"(default for local developement)
SECRET_KEY="secret_key"(odovzdám)
``` 