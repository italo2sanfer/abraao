# Abraham
Django for general use.

# Accessing mysql
```
$ mysql --ssl=FALSE -u root -h db_mysql -p
MySQL [(none)]> Show databases
MySQL [(none)]> select user from mysql.user;
MySQL [(none)]> quit
mysql --ssl=FALSE abraao -u abraao -h db_mysql -p
MySQL [abraao]> show tables;
```

# Create superuser
```
$ python manage.py createsuperuser
```

# Backup/Restore data
```
$ python manage.py loaddata moises/fixtures/pass_data.json
$ python manage.py dumpdata moises.service --indent 2 > moises/fixtures/db_service.json
```

Comando que exporta em json e csv com data e hora
```
$ python manage.py export_models
```

# Create Abraao structure from a GitHub image
```
$ docker network create abraao-network
$ docker run -it --name mysql-go -p 3307:3306/tcp --network abraao-network --env-file .env mysql:8.0
$ # Find the IP address of MySQL and enter it in env file.
$ docker run -it --name abraao-go -p 8002:8002  --network abraao-network --env-file .env ghcr.io/italo2sanfer/abraao:0.5
```
