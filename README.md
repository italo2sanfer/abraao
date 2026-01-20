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