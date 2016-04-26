# django-basic-aws-template

## Getting started

### Downloading the Repository and installing requirements
```
git clone https://github.com/harvard-vpal/django-basic-aws-template.git
cd django-basic-aws-template
pip install -r requirements.txt
```

### Start the web app
Run the web app locally using
```
python manage.py runserver
```
and open (http://localhost:8000/example_app)[http://localhost:8000/example_app]


## The Django app
Check out example_app/views.py and example_app/urls.py


## Deploying on AWS Elastic Beanstalk

[Official documentation from Amazon](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html#python-django-deploy)

### Install the EB CLI
```
pip install awsebcli
```
[More info](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install.html)

### Deploy
```
# initialize, prompts for setup options
eb init

# deploy to amazon
eb create 
```