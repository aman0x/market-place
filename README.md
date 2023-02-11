# Project-X

### Install pytohon 3

    - Install Pip and Virtual Env:
    - https://itsfoss.com/install-pip-ubuntu/
    - OR https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/
    - pip --version
    - virtualenv venv
    - source venv/bin/activate
    - sudo pip3 install -r requirements.txt
    - psycopg: Error: b'You need to install postgresql-server-dev-X.Y for building a server-side extension or libpq-dev for building a client-side application.\n'
    - sudo apt-get install libpq-dev
    - https://www.digitalocean.com/community/tutorials/how-to-install-the-django-web-framework-on-ubuntu-18-04

### Install Django:

    - sudo -H pip install --user Django
    - pip3 install django
    - pip freeze | grep django
    - python -m django --version

### Install Postgres:
    
    - sudo apt-get install postgresql postgresql-client
    - sudo su - postgres
    - psql
    - create database mwb;
    - \l -- list of database
    - CREATE USER root WITH PASSWORD '';
    - GRANT ALL ON DATABASE mwb TO root;
    - sudo service postgresql start -- Start the PostgreSQL server
    - sudo service postgresql stop -- Stop the PostgreSQL server:

### Django REST framework Setup: 
    -pip install djangorestframework
    - pip install markdown       
    - pip install django-filter  
    
>Update settings.py:

    INSTALLED_APPS = [
    ...
    'rest_framework',
    ]

### After Server Setup: 

    - sudo apt-get install postgresql postgresql-contrib
    - sudo apt-get install libpq-dev # this is required as psycopg2 uses pg_config
    - sudo apt-get install python-dev
    - sudo apt-get install python-pip
    - Need python3 dev also --
    - apt-get install python3-dev

### Run Project:

    - python manage.py runserver
    - python manage.py
    - nano ~/myproject/myproject/settings.py --database setings update
    - python manage.py collectstatic
    - python manage.py makemigrations
    - python manage.py migrate
    - python manage.py createsuperuser
    - python manage.py runserver

### To Create New App:
    - python manage.py startapp mwb

### To solve postgres missing error:

    - sudo apt-get install postgresql
    - sudo apt-get install python-psycopg2
    - sudo apt-get install libpq-dev


### Missing -lssl in Mac

    - env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip install psycopg2


### For Gunicron Setup

    - https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-18-04
    - ExecStart=/home/ubuntu/mwb/bin/activate
    - ExecStart=/home/ubuntu/mwb/mwb/bin/gunicorn \



### Static File Serve: 
>Static file not loading Issue Nginx:

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/ubuntu/www/mwb/mwb/static;
    }
    /home/ubuntu/www/mwb/mwb/static


### Error Hint
    - Gunicorn: sudo journalctl -u gunicorn.socket
    - pip: which pip





###Database:
    - User
    - Account
      - Vendor
      - Customer
    
    
    - Item 
    
    - Bucket 
    - #one to many Item #Many to one vendor id

    - Category     
    - Subcategory 


    - Order #to store order history
    - Invoice #To store Order Invoice 
    - Locality #Oberoi Splendor
    - Session

    - Vendor Item Master

    - Device


#Secret
    - postgres password  : mwb@!23
    - Key file mwb