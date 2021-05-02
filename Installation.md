# Instalation 

Quick guide to install odoo on mac

More info on [Odoo Documentation](https://www.odoo.com/documentation/14.0/setup/install.html#source-install)

***This guide doesn't include the PostgreSQL installation.***

***Ps: I'm using the alias python for python3***

Clone the Community version and enter the dir to start doing stuff

```
git clone https://github.com/odoo/odoo.git myodoo
cd myodoo
```

Set the version 

```
git branch --list
git branch checkout 13.0 (or whatever version available)
```

Create the environment
For odoo 13 and 14, only Python 3.7 works fine (take a look at the requirements.txt to make sure of it)

```
# Use pyenv to change the version at the time of creation
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

Install non-python dependencies

```
xcode-select --install
```

Add the config file ```.odoorc``` to root folder


```
[options]
; This is the password that allows database operations:
; admin_passwd = 
; db_host = 
; db_port = 
; db_user = 
; db_password = 
; db_user = 
; db_name = 

; Set the full path to this folder (you can create if it doesn't exists and the name is up to you). It'll contain the filestore, .cache, fontconfig, sessions etc
; E.g. User/name/path/to/odoo/data_dir
; data_dir = 

; Set all addons full paths including odoo's addons (comma separated)
; E.g. User/name/path/to/odoo/addon,User/name/path/to/odoo/another_addon
;addons_path = 
```

If you have backups to be restored, create a backups folder in the root folder and place your backups (.zip, .gzip, sql files) there

Clone the RestoreDump.py into the root folder and run it

Ps: Before running RestoreDump.py, disconnect all sessions from PostgresSQL (postico or other db management, stop the running servers etc)

```
python RestoreDump.py
```
Depending on the size of the file, it may take a while.


Start the server with our custom configuration

> The default configuration file is :file:`{$HOME}/.odoorc` which can be overridden using :option:`--config <odoo-bin -c>`. 
> Specifying :option:`--save <odoo-bin -s>` will save the current configuration state back to that file.


```
# Default
./odoo-bin


# In our case:
./odoo-bin -c .odoorc
```

The odoo server will be running on default port: 8069 (localhost:8069)
