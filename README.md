# Mission Bit Web Portal

<img src="https://avatars3.githubusercontent.com/u/5872193?s=280&v=4" align="right"
     title="Mission Bit Logo" width="120" height="120">

This project will become an interactive web portal system for Mission Bit staff, students, teachers, and volunteers.  This branch is for authorization system setup.  Users will be able to login to the system with their Gmail account, or login with a username and password.  When a user logs into the system with their Gmail account for the first time, they will complete registration and be able to use their Gmail to login thereafter.  A user can also register as either a student or a volunteer

## Getting Started

### Prerequisites

The following are the libraries you'll need in order for this to work on your machine and the commands necessary to install each of them, ommitted but necessary are `python`, `pip` and `postgresql`. 

```
certifi==2019.3.9
chardet==3.0.4
coverage==4.5.3
defusedxml==0.6.0
Django==2.2.1
django-crispy-forms==1.7.2
idna==2.8
oauthlib==3.0.1
psycopg2==2.8.2
PyJWT==1.7.1
python-dotenv==0.10.2
python3-openid==3.1.0
pytz==2019.1
requests==2.22.0
requests-oauthlib==1.2.0
six==1.12.0
social-auth-app-django==3.1.0
social-auth-core==3.2.0
sqlparse==0.3.0
urllib3==1.25.3
```

### Installing

First clone the project, and navigate to your project folder:

```
git clone https://github.com/tylerIams/MB_Portal.git
cd MB_Portal
```

Next, create your virtual environment, and activate it:

```
virtualenv <name>
source <name>/bin/activate
```

Next, (also in your project folder) install all of the necessary dependencies from the project `requirements.txt` file:

```
pip install -r requirements.txt 
```

Finally run the application on your local machine with:

```
python manage.py runserver
```

Navigate in your browser to:

```
localhost:8000/
```

And Bob's your uncle.

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

See also the list of [contributors](https://github.com/tylerIams/MB_Portal/contributors) who participated in this project.

## License

NA

## Acknowledgments

* Thank you Bob Ipollito and Juliana De Heer

