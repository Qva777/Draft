pip freeze > requirements.txt <br>
check
<hr>
<h4>dumpdata and loaddata:</h4>
makemigrations
migrate
python3 manage.py dumpdata --format=json E_Shop_API > mydemodata.json
<br>
python3 manage.py loaddata mydemodata.json


python3 manage.py dumpdata --format=json --indent 4 E_Shop_API > mydemodata.json
<br>
python3 manage.py loaddata mydemodata.json




```
python3 manage.py dumpdata --format=json --indent 4 E_Shop_API > mydemodata.json
python manage.py dumpdata E_Shop_Products --indent 4 > mydemodata.json

```

```
python3 manage.py loaddata mydemodata.json
```
maybe
python3 manage.py loaddata My_fixtures/mydemodata.json








<h1>How to connect Stripe?</h1>
<h4>Go here and register your profile </h4>
<a href="https://dashboard.stripe.com/login"> sign up Stripe</a>





test card
Visa: 4242 4242 4242 4242
Mastercard: 5105 1051 0510 5100
American Express: 3782 822463 10005
Discover: 6011 1111 1111 1117





celery worker:
celery -A E_Shop_config worker --loglevel=info


celery beat:
celery -A E_Shop_config beat --loglevel=info

Redis:
redis-server


commit:
git commit --date="2023-06-14T12:00:00" -m "Updated"
                   year-month-day



отменить последний коммит сохранив данные  
git reset --soft HEAD~1


git commit --date="2023-06-16T12:00:00" -m "Updated"
git commit --date="2023-06-17T12:00:00" -m "Updated"
git commit --date="2023-06-18T12:00:00" -m "Updated"
git commit --date="2023-06-19T12:00:00" -m "Updated"
git commit --date="2023-06-20T12:00:00" -m "Updated"
git commit --date="2023-06-21T12:00:00" -m "Updated"
git commit --date="2023-06-22T12:00:00" -m "Updated"


