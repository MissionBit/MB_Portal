# Mission Bit Web Portal

<img src="https://avatars3.githubusercontent.com/u/5872193?s=280&v=4" align="right"
     title="Mission Bit Logo" width="120" height="120">

This project will become an interactive web portal system for Mission Bit staff, students, teachers, and volunteers.  This branch is for authorization system setup.  Users will be able to login to the system with their Gmail account, or login with a username and password.  When a user logs into the system with their Gmail account for the first time, they will complete registration and be able to use their Gmail to login thereafter.  A user can also register as either a student or a volunteer

## Getting Started

### Prerequisites

`python`, `pip`, `virtualenv` and `postgresql` are prerequisites to installing. Python dependencies will be installed from `requirements.txt` using `pip`. If you're brand new to python, see [Getting Started With Mission Bit and Python Django](#getting-started-with-mission-bit-and-python-django).

### Installing

First clone the project, and navigate to your project folder:

```
git clone https://github.com/tylerIams/MB_Portal.git
cd MB_Portal
git checkout auth
```

Next, create your virtual environment, and activate it:

```
virtualenv venv
source venv/bin/activate
```

Next, (also in your project folder) install all of the necessary dependencies from the project `requirements.txt` file:

```
pip install -r requirements.txt
```

Create the database and apply any necessary migrations:

```
python manage.py migrate
```

Next, seed your database with some data:

```
python manage.py loaddata fixtures.json
```

Once you've seeded the database, you will be able to log in with
either a staff account, student account, or teacher account, with usernames
'staff_user', 'student_user', and teacher_user, respectively.  All three account
passwords are 'topsecret123'

Finally run the application on your local machine with:

```
python manage.py runserver
```

Navigate in your browser to:

```
localhost:8000/
```

## Running the tests

Your requirements.txt file has installed the `coverage` package for you, which provides a nice coverage report for all the tests.

### Run tests

To run tests with the `coverage` library, in your project directory run:

```
coverage run manage.py test tests -v 2
```

After the tests have run, generate a `coverage` report with:

```
coverage html
```

A directory has been created with your `coverage` report called `htmlcov`, to view the coverage run:

```
open htmlcov/index.html
```

Click into any of the modules for a detailed report on the coverage of the tests.  Enjoy!

## Built With

* [Django](https://docs.djangoproject.com/en/2.2/) - Django - the web framework used

## Contributing

NA

## Versioning

NA

## Authors

* **Tyler Iams** - *Initial work*
* **Bob Ippolito** - *Initial editing*
* **Juliana de Heer** - *Editing*

See also the list of [contributors](https://github.com/tylerIams/MB_Portal/contributors) who participated in this project.

## License

NA

## Acknowledgments

* Thank you Bob Ippolito and Juliana de Heer for their ideation and guidance on this project.

## Developing with docker-compose

Using docker-compose, it's not necessary to have a local installation of
Python, PostgreSQL, or anything but
[Docker Desktop](https://www.docker.com/products/docker-desktop)
(or a Linux installation of docker-compose). Conveniently, we can also use
this to run emulated versions of services we depend on such as Azure Storage.

First, apply the migrations
```
docker-compose run web python manage.py migrate
```

Then seed your database with some data:
```
docker-compose run web python manage.py loaddata fixtures.json
```

This will start up the Django server, PostgreSQL database, and
Azure Storage server accessible at
[http://localhost:8000/](http://localhost:8000/):

```bash
docker-compose up
```

Once you've seeded the database and started your container, you will be able to log in with
either a staff account, student account, or teacher account using usernames
'staff_user', 'student_user', and teacher_user, respectively.  All three account
passwords are 'topsecret123'.  Enjoy!

To start over with a fresh environment:

```bash
docker-compose down --volumes
```

You can run Django commands through this environment using docker-compose as
well, such as:

```bash
docker-compose run web python manage.py createsuperuser
```

or:

```bash
docker-compose run web python manage.py makemigrations
```

## Getting Started With Mission Bit and Python-Django

Welcome!  These instructions will help you get started with Python Django and use our Mission Bit web app all in one.  Use these if you've never used Python before on your computer!  Be excited!

First, open a `Terminal` window on your computer.  This will start you off in your computer's home directory (folder), and this is precisely where we want to be to set up the app.  Copy this command and press `return` (enter), then enter again when you're prompted to complete Homebrew installation, which will help you install python:

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Next, install `Python` on your computer (the latest version is called `Python3`) by copying and running this command:

```
brew install python
```

Next, install `pip` which will help you install your virtual environment to run your app (when prompted enter your password for your computer)

```
sudo easy_install pip
```

Next, install `virtualenv`, the package that will allow you to create virtual environments :

```
sudo pip install virtualenv
```

Now you should be ready to start the `Installing` section, only a few commands away from using the Mission Bit web portal!



