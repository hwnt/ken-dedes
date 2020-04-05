# Ken Dedes 

It's Haiwanita backend system!

### Pre-Requisites

If you want to run this code, you have some pre-requisites:
- Docker
- Python 3.7 + 
- MariaDB/MySQL server (Or you can use docker instance by run the docker-compose.yml)

### How to Run

First, you have to have MariaDB/MySQL instance live!
You can either install manually or run by docker.

first you have to env variable `DB_ROOT_PASSWORD=your-own-pw`, `DB_USER=your-username`, `DB_PASSWORD=your-own-pw`, `DB_NAME_PRODUCTION=your_db_name`. then you can run this command:

```
    $ docker-compose up
```

after DB instance live, you can run this code by python command:

```
    $ pip install -r requirements // install the required module in python environment
    $ python3 run.py db migrate // if you dont have the table of db, you can migrate first
    $ python3 run.py 
```

or you can run it by docker:

```
    $ docker build -t kendedes:latest .
    $ docker --name kendedes -p 5000:5000 kendedes:latest
```