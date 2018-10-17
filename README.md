Authors Haven - A Social platform for the creative at heart.
=======

[![Build Status](https://travis-ci.org/andela/ah-backend-stark.svg?branch=develop)](https://travis-ci.org/andela/ah-backend-stark)
 [![Coverage Status](https://coveralls.io/repos/github/andela/ah-backend-stark/badge.svg?branch=develop)](https://coveralls.io/github/andela/ah-backend-stark?branch=develop)

## Vision
Create a community of like minded authors to foster inspiration and innovation
by leveraging the modern web.



## Getting started
### Prerequisites
- [Python 3.6](https://www.python.org/getit/)
- [Postgres database]( https://www.postgresql.org/download/)
- [Pip](https://pip.pypa.io/en/stable/reference/pip_download/) or any other python package manager

### Technologies used
- [Django](https://docs.djangoproject.com/en/2.1/) 
- [Pycodestyle](http://pycodestyle.pycqa.org/en/latest/intro.html)

## Setting up the application


Clone the project repo to your prefered location

`$ git clone https://github.com/andela/ah-backend-stark.git`

Install a virtual environment via pip or prefered package manager

`$ pip install virtualenv`

Create a virtual environment. "env" can be any name

`$ virtualenv env`

Activate environment

- On Windows `$ env\scripts\activate`

- On Mac OS `$ source env/bin/activate`

Install dependencies

`$ pip install -r requirements.txt`



## Database Setup

Rename the .env.example file to .env and change the dummy fields to your respective database connection credencials

Make migrations

` $ python manage.py makemigrations`

` $ python manage.py migrate`

## Running Tests
` $ python manage.py tests`

Tests with coverage

` $ coverage run --source=authors/ manage.py test`

`$ coverage report -m`

## Test the application

Run server

`$ python manage.py runserver`

Endpoints that can be tested on [Postman](https://www.getpostman.com/apps)

[Documentation]() on how to test the endpoints

|Method |Endpoint |Functionality  |
|----------|:----------|------------|
| POST  |/api/users/  |Register user  |
| POST  |/api/users/login/  |Login a user  |
|POST | /api/users/activate_account/:token/  | Verify user account|
| GET | /api/user| Get current user|
| GET |/api/profiles/:username/ | Get user profile |
|PUT|/api/profiles/:username/ |Update profile |
|POST|/api/articles/|Create article|
|GET|/api/articles/|List articles |
|GET|/api/articles/:slug/|Get article|
|PUT|/api/articles/:slug/|Update article|
|DELETE|/api/articles/:slug/|Delete article|
|POST|/api/articles/:slug/comments/|Add comments to an article|
|GET|/api/articles/:slug/comments/|Get comments from an article|
|DELETE|/api/articles/:slug/comments/:id/|Delete comment|
|POST|/api/articles/:slug/favorite/|Favourite articles|
|DELETE|/api/articles/:slug/favorite/|Unfavourite articles|
|GET|/api/articles/favourites/|List favourated articles|
|POST|/api/articles/:slug/like/|Like articles|
|PUT|/api/articles/:slug/like/|Unlike articles|
|POST|/api/profiles/:username/follow/|Follow user|
|DELETE|/api/profiles/:username/unfollow/|Unfollow user|
|PUT|/api/articles/:slug/rate_article/|Rate aricle|


## Deployment site

[Heroku](https://ah-backend-stark-staging.herokuapp.com/)