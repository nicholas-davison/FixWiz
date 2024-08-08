# FizWiz

Fixwiz is a platform to facilitate connections between contractors and customers. Community members post service requests of various types as they arise, and repair people claim these jobs and have a source of business to grow their client base.

## Installation

Make sure you have the following installed:

- python3 3.9
- pipenv

Clone this repository on Github.

Navigate to the fixproject directory and activate a virtual environment using ```pipenv shell``` . Then run the following commands one at a time:

```
pipenv install

./seed_database.sh

python manage.py runserver
```

Finally, follow the instructions on the client side repository: https://github.com/nicholas-davison/FixWiz-Client
