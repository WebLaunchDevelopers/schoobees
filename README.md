# Django-School-Management-System

This app is meant to be used by school manager to manage their school records:
student data
staff
results and
finances.

It currently doesn't allow students/staff to login.
Solely, it's expected to be used on a single machine or online for managers only.


username: admin
password: admin123 / C
```


Run

```python
pip install -r requirements.txt #install required packages
python manage.py makemigrations
python manage.py migrate # run first migration
python manage.py runserver # run the server
```
Then locate http://172.0.0.1:8000

## Admin Login
When you run migrate, a superuser is created.
```bash
username: admin
password: admin123
```

## Roadmap
To build a fully fledged open source school management.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Coding Standards
```bash
isort .
black .
```

## Test
```base
python manage.py test
```

## Delete __pycache__ Cache files
```
use this command in "cmd" of windows in root folder
for /d /r . %d in (__pycache__) do @if exist "%d" rd /s /q "%d"
OR
use this command in "cmd" of Linux in root folder
sudo find . -type d -name '__pycache__' -exec rm -rf {} +
```

## Delete files inside migrations folder excluding __init__.py
```
use this command in "cmd" of windows in root folder
for /r . %d in (migrations\*.py) do @if "%~nxd" neq "__init__.py" del /s /q "%~fd"
OR
use this command in "cmd" of Linux in root folder
find . -path "*/migrations/*.py" ! -name "__init__.py" -delete

```

## Delete db.sqlite3
```
use this command in "cmd" of windows in root folder
del /q db.sqlite3
OR
use this command in "cmd" of Linux in root folder
rm db.sqlite3
```

# To change GIT URL
```
git remote set-url origin <new remote URL>
```

# Virtual ENV
```
virtualenv myenv
myenv\Scripts\activate
```