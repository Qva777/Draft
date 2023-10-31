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
            
  - run 3 commands
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




user admin :
            admin@gmail.com
            Testpass1
basic user : 
            user@gmail.com
            Testpass1