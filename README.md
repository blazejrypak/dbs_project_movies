    Install pipenv
    $ sudo apt install pipenv
    Installing dependencies from Pipfile.lock...
    $ pipenv install 
    To activate this project's virtualenv, run the following:
    $ pipenv shell
    
    $ cd movie_projx 
    $ python manage.py migrate
    $ python manage.py makemigrations movie_app
    $ python manage.py migrate
    $ python manage.py createsuperuser
    $ python manage.py runserver
