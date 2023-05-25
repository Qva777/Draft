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
```

```
python3 manage.py loaddata mydemodata.json
```
maybe
python3 manage.py loaddata My_fixtures/mydemodata.json



Mandatory Variables
BOT_TOKEN: Create a bot using @BotFather, and get the Telegram API token.

API_ID: Get at my.telegram.org/apps.

API_HASH: Get at my.telegram.org/apps.

DATA_BASE_URL: If you have a database then url here. If you dont have one then bot will create one for you in heroku.




<h1>How to connect Stripe?</h1>
<h4>Go here and register your profile </h4>
<a href="https://dashboard.stripe.com/login"> sign up Stripe</a>
