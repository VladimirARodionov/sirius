# Sirius CRM

Setup development environment
---

 - Install python, pip, npm
 - Clone the project

```
pip install -r requirements.txt 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata defaults.json
python manage.py loaddata cities_light_country.json
python manage.py loaddata cities_light_region.json
python manage.py loaddata cities_light_city.json
python manage.py runserver 127.0.0.1:8000

cd frontend
npm install
npm run dev
```

Setup production on Ubuntu or Debian
---
 - Install python, pip, npm
 - Clone the project
 ```
apt-get install python3-venv
apt-get install libapache2-mod-wsgi-py3
python3 -m venv sirius
source sirius/bin/activate
cd sirius
pip install -r requirements.txt 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata defaults.json
python manage.py loaddata cities_light_country.json
python manage.py loaddata cities_light_region.json
python manage.py loaddata cities_light_city.json

cd frontend
npm install
npm run build
```

Configure Apache
---

 - in /etc/apache2/sites-available/ create following file with name sirius.conf
```
WSGIScriptAlias /crm <web folder>/sirius/Sirius/wsgi.py process-group=server.raevskyschool.ru
WSGIDaemonProcess server.raevskyschool.ru python-home=<web folder>/sirius/ python-path=<web folder>/sirius/bin:<web folder>/sirius/lib/python3.6/site-packages:<web folder>/sirius/ socket-user=#501
WSGIProcessGroup server.raevskyschool.ru
WSGIApplicationGroup %{GLOBAL}
WSGIScriptReloading On
WSGIPassAuthorization On

<Directory <web folder>/sirius/Sirius>
<Files wsgi.py>
Require all granted
</Files>
</Directory>

Alias /sirius <web folder>/sirius/frontend/dist/

<Directory <web folder>/sirius/frontend/dist/>
AllowOverride All
Require all granted
FallbackResource index.html
</Directory>

Alias /static <web folder>/sirius/frontend/dist/static/

<Directory <web folder>/sirius/frontend/dist/static/>
Require all granted
</Directory>
```
 - create symbolink link to this file in /etc/apache2/sites-enabled/
 ```
 cd /etc/apache2/sites-enabled
 ln -s /etc/apache2/sites-available/sirius.conf
 ```
 
  - in the folder containing web resources create following file with name .htaccess
  ```
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /sirius
  RewriteRule ^sirius/index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /sirius/index.html [L]
</IfModule>
 ``` 
  - restart apache service
  
If you want to change web server URL:
---
 - replace server.raevskyschool.ru to your URL in the configs above
 - replace server.raevskyschool.ru in settings.py EMAIL_HOST property to your SMTP server name
 - replace 501 in socket-user=#501 to apache user PID 