# Graveyard: Place for Dead (and Undead)

Graveyard is an attempt at open-source reimplementation of [DraciDoupe.cz](https://www.dracidoupe.cz/) (referred to as DDCZ in this text).

Developer's documentation is [at Read the Docs](https://ddcz.readthedocs.io/en/latest/). 

Production will be running at http://nove.dracidoupe.cz/

## Contributions

Contributions are welcome provided you agree your work will be shared under the same license as Graveyard (MIT).

If you don't know where to start, take a look at issues or ask Almad on [development Slack](https://dracidoupe.slack.com/messages/C7F0YCTFU) or in Pošta on [DraciDoupe.cz](https://www.dracidoupe.cz/). 

## Installation

You can run Graveyard either directly on your machine or inside [Docker](https://www.docker.com/).

Installing and running Graveyard directly is faster (on some systems) and removes one lever of indirection, but it makes the setup more complicated. 

Running in Docker requires familiarity with it, but it makes setup easier and guarantees consistency with the testing environment (and hopefully in the future, production environment as well). 

In both cases, first clone this repository and run all commands in its directory.

### Installing in Docker

Requirements:

* You have [Docker CE installed](https://www.docker.com/community-edition)
* You have [installed docker-compose](https://docs.docker.com/compose/install/)

* Create your own copy of [local configuration](graveyard/settings/local.example.py)

  * `cp graveyard/settings/local.example.py graveyard/settings/local.py`

Verify you have everything ready by running the test suite:

* `docker-compose run web python3 manage.py test`

If you see output like this:

```
(graveyard-venv) almad@zeruel:~/projects/graveyard$ docker-compose run web python3 manage.py test
Starting graveyard_db_1 ... done
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
Destroying test database for alias 'default'...
(graveyard-venv) almad@zeruel:~/projects/graveyard$ 

```

You are all set. Afterwards, install database schema by running

*  `docker-compose run web python3 manage.py migrate`

and load data about pages

*  `docker-compose run web python3 manage.py loaddata pages`

You are done! Now you can just run the project and develop using

*  `docker-compose start`

Verify your application works and open `http://localhost:8000` (`localhost` may be a different host if you are not working on linux). If so, create yourself a superuser

*  `docker-compose run web python3 manage.py createsuperuser`

and then review content at `http://localhost:8000/admin/`

### Installing on your machine

Graveyard is currently written in [Django](https://www.djangoproject.com/). Requirements to develop it:

* You have working Python 3 installation on your machine
* You have working MySQL installation on your machine

To use the project, clone this repository, enter its directory with `cd graveyard` and:

* Create a virtual environment: `python3 -m venv gvenv`
   * If this fails and you are on Ubuntu, you may need to `sudo apt-get update && sudo apt-get install python3-pip && sudo pip3 install virtualenv`
* Enter it (on Mac OS X or Linux): `source gvenv/bin/activate`
* Install dependencies within the `pip install -r requirements.txt`
* Copy settings template: `cp graveyard/settings/local.example.py graveyard/settings/local.py`
* Edit the settings above, especially enter credentials to your local MySQL ([see Stack Overflow](https://stackoverflow.com/questions/1720244/create-new-user-in-mysql-and-give-it-full-access-to-one-database) on how to do that)
* Verify you have correct installation and run tests with `python manage.py test`. You should see output like this:

```
(graveyard-venv) almad@zeruel:~/projects/graveyard$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.031s

OK
Destroying test database for alias 'default'...
(graveyard-venv) almad@zeruel:~/projects/graveyard$ 
```

* Create the database schema: `python manage.py migrate`
* Load data about pages to see what's on production: `python manage.py loaddata pages`
* Run the thing! `python manage.py runserver`
* Observe if you have contact at `http://localhost:8000`
* Maybe create a superuser in order to enter admin: `python manage.py createsuperuser`
* Look around the administration interface at `http://localhost:8000/admin/`

#### Installation issues

*  Installation failes with "mysql_config not found" 

If you get something like this:

```
    File "/tmp/pip-install-wfhe9zue/mysqlclient/setup_posix.py", line 29, in mysql_config
        raise EnvironmentError("%s not found" % (_mysql_config_path,))
    OSError: mysql_config not found
```

you may be using MariaDB fork of MySQL that the Python client is not equipped to talk to, installation-wise. You need to manually symlink the appropriate command:

`ln -s /usr/bin/mariadb_config /usr/bin/mysql_config`

If even `mysql_config` is not there, you have to install development headers for the database. That's `apt-get install libmariadbclient-dev` on Debian.

* `error: invalid command 'bdist_wheel'`

Old setuptools: `pip install setuptools -U`

## Database setup

There are multiple ways how to build forked application. In your local environment you can install your
own MySQL server, or you can use Docker to build it. You can also create your database on remote-server,
we will cover those options here.

The key file is your new file `local.py`, that you have created from `local.example.py` which is ignored
by git. This way you can use this settings only for your local machine and you will not change anything 
on testing or production server.

Your primary goal is to find `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_HOST`
and add those in the local config file.

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DATABASE_NAME',
        'USER': 'DATABASE_USER',
        'HOST': 'DATABASE_HOST',
        'PASSWORD': 'DATABASE_PASSWORD',
        'OPTIONS': {
            'charset': 'latin2'
        },
        'TEST': {
            'NAME': 'test_dracidoupe_cz',
            'CHARSET': 'latin2',
        }
    }
}
```
### General notes
- You can not run tests if you are using only one database (eg remote database created via tools
  like Heroku). To run tests you need to have MySQL server which allows you to creat new databases.
  
- Be aware! _Not all database products can be reached._ Typical example is WEDOS DB, that is reachable
  only an only if you are connecting from within WEDOS apps. You will not be able to make connection
  between your localhost app and this WEDOS DB. There are almost certainly many other products like 
  this one.
  
- We do not use MySQL newer than 5.5 because of the old web version, currently 
  running at `http://dracidoupe.cz`. You can use newer version on your local machine, but to be sure
  everything works fine we recommend to use 5.5.

### Docker Database server
We will use image for MySQL, so we do not have to setup everything by ourselves. Key part is to properly
set the `docker-compose.yml`. We need to register service _db_
``` dockerfile
services:  
  db:
    image: mysql:5.5
    volumes:
      - .db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=docker
      - MYSQL_DATABASE=dracidoupe_cz
```
This service _db_ is created with two environment constants. We can see that `.db` is linked 
to `/var/lib/mysql`, therefore you are free to add some settings for the virtual service db.

If you please to check the database and its tables, you can connect via any tool. The most common
are PhpMyAdmin and Adminer. You add them to your `docker-compose.yml`

```dockerfile
services:  
  db:
    image: mysql:5.5
    volumes:
      - .db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=docker
      - MYSQL_DATABASE=dracidoupe_cz
  adminer:
    image: clue/adminer
    depends_on:
      - db
    ports:
      - 81:80
  phpmyadmin:
    image: phpmyadmin
    depends_on:
      - db
    ports:
      - 82:80
```
This way you can create two new virtual servers that are accessible at `localhost:81` 
and `localhost:82` respectively. To sign in you use _root_ and its password _docker_ 
at host _db_ which reflects the name of the service.


### Heroku ClearDB
Some of us have their app deployment on Heroku which also means we need to connect to the database
there. You can use the remote-database also for your localhost. But be aware of this method.
__To create Heroku ClearDB, you have to put your credit/debit card info into the Heroku.__ Even if you
are using their free product. If you have problems with this, probably do not use Heroku as your 
choise.

- First you have to sign in with your heroku account.

- You create new app by `new -> Create new app` (you can also create pipeline for yourself and then
  create the app in the pipeline).
  
- Open your app and click on `Resources`. In `Add-ons` you can type _ClearDB MySQL_ and it will provide
  you new MySQL database. You have to chose your _Plan name_. Select the on that is free, since
  the database with testing data is not huge. This plan _Ignite Free_ will provide you 5MB of space,
  10 connections and nightly backups. Now (2020-12-19) the database without ddcz data is 1.2MB.
  
If you are using Heroku commands, just type `heroku addons:create cleardb:ignite`.

- With created database go to `Settings` and find section names `Config Vars`.

- Click on `Reveal Config vars` and you will get constant `CLEARDB_DATABASE_URL`. This way you will get
  url in shape `mysql://DATABASE_USER:DATABASE_PASSWORD@DATABASE_HOST/DATABASE_NAME?reconnect=true`. You can
  put those data into your `local.py` and you can test by running the migrations.
  










