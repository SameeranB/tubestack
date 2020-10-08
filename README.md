# TubeStack

> A quicker way to stay updated with your YouTube feed.

[![Build Status](https://travis-ci.com/SameeranB/tubestack_backend.svg?branch=master)](https://travis-ci.com/SameeranB/tubestack_backend)
---
You can find the API documentation [here](https://documenter.getpostman.com/view/8369112/TVRj4nu3).

## Instructions

---
### With Docker
1. Clone the repository.
2. Run this command: `docker-compose -f Docker/docker-compose.dev.yml up --build`. This may take some time.
3. You should be able to access the API at `localhost:8000`.


### Without Docker
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
## Additional Information

* An Admin account is automatically created when the docker container is run. The default credentials for which can be set in the environment file.
* Please ensure that `DOCKER=0` is present in your environment file if you are not using docker, the `settings.py` file will implement certain changes accordingly. Similary for `DOCKER=1` when using Docker.
* The admin panel has been configured to display video information and sorting-searching options.I ran out of time and couldn't make a seperate dashboard.
