# Instalation

Download the [Community version](git clone https://github.com/odoo/odoo.git)

Create venv 3.7 (it doesn't work with newer versions, use pyenv to change)

```
pyenv global 3.7
python -m venv .venv
```

Activate env

```
. .venv/bin/activate (mac)
. .venv/Scripts/activate (windows git bash)

```

Install dependencies

```
pip install setuptools wheel
pip install -r requirements.txt
pip install psycopg2-binary
```

Add the config file to root folder

```
[options]
; This is the password that allows database operations:
; admin_passwd = admin
; db_host = False
; db_port = False
; db_user = odoo
; db_password = 
; db_user = 
; db_name = 

; This folder will contain the filestore, .cache, fontconfig, sessions etc
; data_dir = 

; Set all custom addons path. E.g.: odoo's root addons and enterprise
;addons_path = 
```

If you have a backups folder at root folder with .zip, .gzip, sql files, copy/create the RestoreDump.py on the root folder and run it

```
python RestoreDump.py
```
