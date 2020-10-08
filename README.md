# TubeStack

> A quicker way to stay updated with your YouTube feed.

[![Build Status](https://travis-ci.com/SameeranB/tubestack_backend.svg?branch=master)](https://travis-ci.com/SameeranB/tubestack_backend)
---
You can find the API documentation [here](https://documenter.getpostman.com/view/8369112/TVRj4nu3).

## Features:
* User Registration and Authentication using Django Tokens.
* Every user can choose their keyword and can also change them at any time.
* Backend syncs with YouTube every 20 seconds.
* Video and Keyword storage is optimized for multiple users. Redundancy is minimum: `VideoData` is never repeated, the same `Keywords` are never stored more than once.
* Uses RabbitMQ for celery task scheduling. Very Scalable.
* Custom client wrapper for Google API Client.
* Containerized Using Docker.
* Automatic invalidation of quota-exceeded API tokens
* Ability to add new tokens as an Admin
* Ability to list all tokens.
* Django Admin Panel comes configured with searching and filtering options. Find it at: `localhost:8000/admin`

---

## Instructions

---
### With Docker
1. Clone the repository.
2. Ensure that `DOCKER=1` is set in your .env file.
3. Run this command: `docker-compose -f Docker/docker-compose.dev.yml up --build`. This may take some time.
4. You should be able to access the API at `localhost:8000`.


### Without Docker
1. Clone the repository.
2. Set up your virtual environement and run `pip install -r requirements.txt`.
3. Ensure that `DOCKER=0` is set in your .env file.
4. You will have to set up RabbitMQ on your system. Follow these steps:
   * run `sudo apt-get install rabbitmq-server`
   * run `sudo rabbitmqctl add_user rabbit mypassword`
   * run `sudo rabbitmqctl add_vhost tubestackhost`
   * run `sudo rabbitmqctl set_permissions -p tubestackhost rabbit ".*" ".*" ".*"`

5. Collect the static files using `python manage.py collectstatic`
6. Apply the migrations using `python manage.py migrate`
7. Create a superuser and the initial Youtube Token using `python manage.py initadmin`
8. Run 3 seperate terminal windows, with the following commands:
   * run `celery -A tubestack_backend worker -l info` to activate the worker.
   * run `celery -A tubestack_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler` to activate the scheduler.
   * run `python manage.py runserver` to run the DRF server.

---
## Additional Information

* Please use fresh API Tokens when adding them to the system. The validity of the token is calculated based on the number of times it is used.
* An Admin account is automatically created when the docker container is run. The default credentials for which can be set in the environment file.
* Please ensure that `DOCKER=0` is present in your environment file if you are not using docker, the `settings.py` file will implement certain changes accordingly. Similary for `DOCKER=1` when using Docker.
* The admin panel has been configured to display video information and sorting-searching options.I ran out of time and couldn't make a seperate dashboard.
