# Voxie

A smart voice assistant online.

- Front end
- Back end

Address of Swagger API: http://127.0.0.1:5000/api/docs/


Main Directories：

- `app`：Flask APP
- `config.py`：Flask App Configuration
- `manage.py`：Flask App Management
- `requirements.txt`：Python Packages
- `run_app.sh`：Base on Gunicorn
- `fabfile.py`：Fabric automation deployment


# Config

## development Config

1. Create Python environment and install packages

Windows PowerShell：

```
PS > python3 -m venv ./venv
PS > .\venv\Scripts\Activate.ps1
(venv) PS > pip3 install -r requirements.txt
```

Linux：

```sh
$ python3 -m venv ./venv
$ source venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

2. Create DB and admin user

```sh
(venv) > python manage.py db_createfirst
drop the database?[y/n]: n
The database is created successfully!
Please Enter the superuser username:admin
Password:123456
Confirm password:123456
Superuser is created successfully!
```

3. Only create the admin

```sh
(venv) > python manage.py createsuperuser
Please Enter the superuser username:admin2
Password:123
Confirm password:123
Superuser is created successfully!
```

3. Start the server

```sh
(venv) > python manage.py runserver
```





