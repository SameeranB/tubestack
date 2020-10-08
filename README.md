# TubeStack

> A quicker way to stay updated with your YouTube feed.
[![Build Status](https://travis-ci.com/SameeranB/tubestack_backend.svg?branch=master)](https://travis-ci.com/SameeranB/tubestack_backend)
---
You can find the API documentation [here](https://documenter.getpostman.com/view/8369112/TVRj4nu3).

## Instructions

---

1. Clone the repository.
2. Set up your virtual environement and run `pip install -r requirements.txt`.
3. You will have to set up RabbitMQ on your system. Follow these steps:
   * run `sudo apt-get install rabbitmq-server`
   * run `sudo rabbitmqctl add_user rabbit mypassword`
   * run `sudo rabbitmqctl add_vhost tubestackhost`
   * run `sudo rabbitmqctl set_permissions -p tubestackhost rabbit ".*" ".*" ".*"`

4. Collect the static files using `python manage.py collectstatic`
5. Apply the migrations using `python manage.py migrate`
6. Create a superuser using `python manage.py createsuperuser`
7. Run 3 seperate terminal windows, with the following commands:
   * run `celery -A tubestack_backend worker -l info` to activate the worker.
   * run `celery -A tubestack_backend beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler` to activate the scheduler.
   * run `python manage.py runserver` to run the DRF server.

---
