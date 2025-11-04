# Abraham
Django for general use.

# Tasks
- Repassar senhas que faltam
- Gerar os arquivos json novamente
- Jogar arquivo modificado no cofre;
- Jogar os jsons no cofre

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

# Backup data
```
$ python manage.py dumpdata passapp.service --indent 2 > passapp/fixtures/db_service.json
```