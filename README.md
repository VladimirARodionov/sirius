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
python manage.py runserver 127.0.0.1:8000

cd frontend
npm install
npm run dev
```
