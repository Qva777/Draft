# E_Shop &middot; [![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

[<img src="E_Shop_config/static/img/logo_dark.png" width="230" height="130">](#)
<!-- ABOUT -->
> E_Shop is an innovative online store with two color themes (light/dark) for user convenience.
> Administrators have the ability to create products and manage them effectively.
> Users can easily add products to the cart, select the required quantity, and also use the implemented payment system
> for
> convenience during shopping.
> The simple and intuitive interface ensures ease of use for all users.
<!-- END ABOUT -->

<hr>

<h1>📍How to install: </h1>

<!-- POSTMAN -->
<details><summary><h2>📮Connect to Postman:</h2></summary><br/>

<h4><b>1.1</b> Import <i>"Postman Collections"</i> folder into Postman</h4>
<h4><b>1.2</b> Set the environment settings <i>"User Data e_shop.postman_environment"</i></h4>
<h4><b>1.3</b> The <i>"E_Shop_API.postman_collection"</i> collection contains requests</h4>
<h4 name="headers"><b>1.4</b> Go to the Google Configuration, select <i>"Change Sites"</i> and set host</h4>

```
http://localhost:8000
```

<h4><b>1.5</b> Select <i>"Social application"</i></h4>
<p>
To integrate the <i>"Social application"</i> with your project, follow these steps:
</p>
<ul>
    <li>Visit <a href="https://console.cloud.google.com/welcome" target="_blank">Google Cloud Console</a> and CREATE PROJECT</li>
    <li>Navigate to <a href="https://console.cloud.google.com/apis/credentials" target="_blank">APIs & Services > Credentials</a></li>
    <li>Click on <b>"Create Credentials"</b> and choose <b>"OAuth client ID"</b></li>
    <li>Specify the application type as <b>"Web application"</b></li>
    <li>Set the name of your client (e.g., "Social App Client")</li>
    <li>Under <b>"Authorized redirect URIs,"</b> add the appropriate redirect URI for your application</li>
    <li>Click <b>"Create"</b> to generate your OAuth client ID and client secret</li>
</ul>
<p>
Once created, copy and securely store the generated <b>Client ID</b> and <b>Client secret</b>.
</p>
<pre>
    Client ID: Your_Client_ID
    Client secret: Your_Client_Secret
</pre>
</details>
<!-- END POSTMAN -->

<!-- MANUAL -->
<details><summary><h2>🔧Manual Installation:</h2></summary><br>
<h3>Connect venv:</h3> 

```
python3 -m venv venv
```

<h3>Activate it:</h3>
<i>For Windows</i>

``` 
.\venv\Scripts\activate
```

<i>For MacOS</i>

``` 
source venv/bin/activate 
```

<h3>Install libraries:</h3>

```
pip install -r requirements.txt
```

<h3>Create Your .env:</h3>

```
# Django configuration
SECRET_KEY=your_secret_key
DEBUG=1  # Set 1 or 0 
#
# PostgreSQL (docker/local)
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=your_db_port
#
# pgadmin container
PGADMIN_DEFAULT_EMAIL=your_pgadmin_email
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
#
# Stripe payment
STRIPE_PUBLIC_KEY=pk_key
STRIPE_SECRET_KEY=sk_key
#
# Settings Gmail SMTP
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

<h3>Create PostgreSQ DB: </h3>
<i>Server > Data Bases > Create DB and give name</i>

```
e_shop_db
```

<h3>Apply migrations:</h3>

```
python manage.py migrate
```

<h3>Install fixtures:</h3>

```
python commands.py
```

<h3>Run Commands:</h3>

<i>Runserver:</i>

```
python manage.py runserver
```

<i>Celery worker:</i>

```
celery -A E_Shop_config worker --loglevel=info
```

<i>Celery beat:</i>

```
celery -A E_Shop_config beat --loglevel=info
```

<h3>Use the following steps for configuration:</h3>
<pre>
Go to Postman installation
• <b>1.4</b> Configure <i>"Change Sites"</i>
• <b>1.5</b> Configure <i>"Social application"</i>
</pre>


Go to Postman installation
[• <b>1.4</b> Configure "Change Sites"](#headers)
[• <b>1.5</b> Configure "Social application"](#headers)  
</details>
<!-- END MANUAL -->

<!-- Docker -->
<details><summary><h2>🐳Connect to Docker Compose:</h2></summary><br/>

<h3>Create Your .env and set correct values:</h3>

```
# Django configuration
SECRET_KEY=your_secret_key
DEBUG=1  # Set 1 or 0 
#
# PostgreSQL (docker/local)
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=your_db_port
#
# pgadmin container
PGADMIN_DEFAULT_EMAIL=your_pgadmin_email
PGADMIN_DEFAULT_PASSWORD=your_pgadmin_password
#
# Stripe payment
STRIPE_PUBLIC_KEY=pk_key
STRIPE_SECRET_KEY=sk_key
#
# Settings Gmail SMTP
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your_email_password
```

<h3>UP Docker-compose:</h3>

```
docker-compose up
```

<h3>Login to the container console:</h3>

```
docker exec -it django-container bash
```

<h3>Apply migrations:</h3>

```
python manage.py migrate
```

<h3>Install fixtures:</h3>

```
python commands.py
```

<h3>Use the following steps for configuration:</h3>
<pre>
Go to Postman installation
• <b>1.4</b> Configure <i>"Change Sites"</i>
• <b>1.5</b> Configure <i>"Social application"</i>
</pre>


</details>
<!-- END Docker -->

<hr>
<h1>📂Detail information about project</h1>

<h3><a href="#">Try the link to the website</a></h3>

<details><summary><h1>📚Additional Information</h1></summary><br/>

<h3>Connect to Stripe</h3>
<p>1. Go to the Stripe registration page and create your profile:</p>
<a href="https://dashboard.stripe.com/login"><b>Sign up for Stripe</b></a>

<p>2. Confirm your account.</p>

<p>3. Navigate to the following link to obtain your API keys and <b>copy</b> them:</p>
<a href="https://dashboard.stripe.com/test/apikeys"><b>Stripe API Keys</b></a>

<p>4. Past to your .env:</p>
<pre>
STRIPE_PUBLIC_KEY=Publishable key
STRIPE_SECRET_KEY=Secret key
</pre>

<h4>Test Cards:</h4>
<ul>
    <li>Visa: 4242 4242 4242 4242</li>
    <li>Mastercard: 5105 1051 0510 5100</li>
    <li>American Express: 3782 822463 10005</li>
    <li>Discover: 6011 1111 1111 1117</li>
</ul>

<h3>Connect to Google SMTP</h3>
<p>1. Create app password at the following link:</p>
<a href="https://myaccount.google.com/apppasswords">Google App Passwords</a>

<p>2. Set the following in your settings:</p>
<pre>
EMAIL_HOST_USER=example@gmail.com
EMAIL_HOST_PASSWORD=example_code
</pre>

<h4>User Credentials:</h4>
<h4 style="text-align: center;">Admin:</h4>

```
admin@gmail.com
```

```
Testpass1
```

<h4 style="text-align: center;">Basic User:</h4>

```
user@gmail.com
```

```
Testpass1
```

</details>

<details><summary><h1>📂Screenshots</h1></summary><br/>
- photo 1
- photo 2
- photo 3
- photo 4
</details>





1 manual install

- create venv
- install requirements
- create .env
- create postgres db
- migrate
- fixtures
  python commands.py
  apply manually
  python3 manage.py loaddata My_fixtures/my_products_data.json
  python3 manage.py loaddata My_fixtures/my_users_data.json

- run 3 commands celery
- postman(run google configuration)
- run tests

2 using docker

- create .env
- docker-compose up
- docker exec -it django-container bash
- migrate
- fixtures
- localhost:5050 create db
    - localhost(5050):
      register Server
      in connection set:
      host: postgres-container
      username: postgres
      password: your_password
- postman (run google configuration)

3 postman

- install environment
- install data
- set data
- run google configuration

4 about

- description
- photos
- try link(hosting)

5 подсказки

```
python manage.py dumpdata E_Shop_Products --indent 4 > mydemodata.json
python manage.py dumpdata E_Shop_Users --indent 4 > my_users_data.json
```

python3 manage.py loaddata My_fixtures/my_products_data.json
python3 manage.py loaddata My_fixtures/my_users_data.json









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
git commit --date="2023-10-30T12:00:00" -m "Updated"
year-month-day

отменить последний коммит сохранив данные  
git reset --soft HEAD~1

sudo lsof -i :5432
sudo kill -9 317  
sudo rm /tmp/.s.PGSQL.5432.lock
sudo rm /tmp/.s.PGSQL.5432             
chmod 1777 /tmp

зайти в контейнер
docker exec -it django-container bash

ssh -R 80:localhost:8000 serveo.net

ssh -o ServerAliveInterval=60 -R QvaShquai.serveo.net:80:localhost:8000 serveo.net