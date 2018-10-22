# Django 2.0 Template for starting a new project

Main features

* Better layout of project
* Postgres DB
* Python decouple (for decoupling dev and prod environments)
* Settings in a folder, for better decoupling
* Logging (of requests, and whatever you want to log)
* List of packages ready to install in requirementes (NOTE: Check them and take out the ones you do not want if you need the installation to be minimal)

## Linux (Ubuntu or Debian) package installation

$ apt-get install git
$ apt-get install nginx

Check python version (should be 3.4 or 3.6)

## Virtual environment


References if you want to read, if not go straight to code
http://levipy.com/virtualenv-and-virtualenvwrapper-tutorial/
Instalatión: http://virtualenvwrapper.readthedocs.io/en/latest/install.html
What is:     http://docs.python-guide.org/en/latest/dev/virtualenvs/


```
$ sudo apt-get install libpq-dev python-dev python-pip
$ sudo pip install virtualenv
$ sudo pip install virtualenvwrapper
$ mkdir ~/.virtualenvs
$ vi ~/.bashrc
export WORKON_HOME=$HOME/.virtualenvs  
source /usr/local/bin/virtualenvwrapper.sh

$ mkvirtualenv --python=python3.6 myproy (if we do not specify python version, it will use the one of de O.S)
$ mkdir myproy ; cd myproy
$ workon myproj
$ setvirtualenvproject $VIRTUAL_ENV $(pwd)   (when we go into virtual env, automatically changes to this dir)
```

## Database

```
$ sudo apt-get update
$ sudo apt-get install -y binutils postgresql postgresql-contrib
# Here it will be asked a password for the database
$ sudo su - postgres
$ psql
> CREATE USER myprojectuser WITH PASSWORD 'password';
> CREATE DATABASE myproject OWNER myprojectuser;
> ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
> ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
> ALTER ROLE myprojectuser SET timezone TO 'UTC';
> GRANT ALL PRIVILEGES ON DATABASE myproject TO myprojectuser;
# Test the connection, quit with \q or ctrl+d
$ psql -h localhost -U myprojectuser myproject

# Install postgis if we are going to use it

# Install required libraries
$ sudo apt-get install binutils libproj-dev gdal-bin
# BE CAREFUL with version, we can look ours with following command
# sudo apt-cache search postgresql | grep gis
$ sudo apt-get install -y postgis postgresql-9.3-postgis-2.1 python-psycopg2
$ sudo -u postgres psql -c "CREATE EXTENSION postgis; CREATE EXTENSION postgis_topology;" myproject  # NEED SUPERUSER
```

Extra references for postgis

Install:
http://www.saintsjd.com/2014/08/13/howto-install-postgis-on-ubuntu-trusty.html

Required libraries:
https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/#geosbuild

Optimizations:
https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-postgis-on-ubuntu-14-0

## Install django and create project

```
$ workon myproj
$ pip install django
$ django-admin.py startproject myproject --template=https://github.com/gonzaloamadio/django-template/archive/master.zip
$ cd myproject
$ pip install -r myproject/requirements/dev.txt
$ mv environment.env.example .env
$ vi .env
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=mydbname
DB_USER=mydbuser
DB_PASSWORD=mydbpass
DB_HOST=localhost

$ cd myproject
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
```

## OPTIONAL : color git branches in terminal

```
 parse_git_branch() {
      git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
  }
 export PS1="\u@\h \[\033[32m\]\w\[\033[33m\]\$(parse_git_branch)\[\033[00m\] $ "
 
 # Color ls
 LS_COLORS=$LS_COLORS:'di=0;94:ln=0;34:ex=0;32' ; export LS_COLORS
```
