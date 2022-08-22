# currency-converter
A FastAPI application for converting currencies to other currencies

## Technologies used
- Server application:
    - [FastAPI](https://fastapi.tiangolo.com/), FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
    - [SQLAlchemy](https://www.sqlalchemy.org/), the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
    - [Alembic](https://alembic.sqlalchemy.org/en/latest/), a lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
    - [PostgreSQL](https://www.postgresql.org/), an open source object-relational database system.
    - [Redis](https://redis.io/), in-memory data store which can be used as a database, cache, streaming engine, and message broker.
    - [OpenAPI](https://www.getpostman.com/), a complete API development environment, and flexibly integrates with the software development cycle for API testing.

## Installation
### Local installation
Running this service locally requires you to install Python, PostgreSQL and Redis. Install them by following the instructions in the link below:
 - Installation directions:
    - I used Python 3.8 as my Python version. You can get that exact version [here](https://www.python.org/downloads/release/python-3810/)
    - Redis can be installed by following the steps on the official website [here](https://redis.io/docs/getting-started/#install-redis)
    - PostgreSQL can be downloaded [here](https://www.postgresql.org/download/)

- Basic installation:
    - Install [Python](https://www.python.org/), [PostgreSQL](https://www.postgresql.org/) adn [Redis](https://redis.io/) on your host environment (or PC).
    - Install [Pipenv](https://pipenv.pypa.io/en/latest/)  which is used to manage the virtual environment using `pip3 install pipenv`.
    - Ensure Git is installed, then clone this repository by running `git clone git@github.com:Lord-sarcastic/currency_converter.git` in the terminal.
    - Enter the directory with `cd `
    - Create a `.env` file using the [.env.example](/.env.example) file as a template. Ensure to fill in appropriate values.
    - Run `pipenv install` to install all necessary dependencies for the server application in a virtual environment.
    - Run `pipenv shell` to activate the virtual environment.
    - With Postgres installed, login to the Postgres terminal with `sudo -u user psql`
    - In the same terminal as above, run the command `create role sasori with login password 'sasori';` to create a user. If you don't want 'sasori` replace it with whatever you want. Ensure you update the .env files accordingly.
    - Next, you run migrations with `alembic upgrade head`.
    - Run the server with `python main.py`. It should be running on port 8000.

### Docker
If you've got Docker installed, edit the `.docker.env` file to your taste (you wouldn't need to except you hate me), then run:
- `docker-compose build` to build the image
- `docker-compose run web alembic upgrade head` to run migrations for the database
- `docker-compose up -d` to spin up the server.

The application should be running on port `8000` at URL: `127.0.0.1:8000`.


## API Enpoints documentation
The application is made up of 6 endpoints in total handling authentication and conversion of money from one currency to another

Documentation for the application is found in `/docs` route where it is in OpenAPI format and you can also test it there.

## Testing 🚨
Automated tests have been written and you can run tests with manual setup using pytest like so:
`pytest .`
You can run the tests on Docker with `docker-compose run web pytest`.

If you insist on testing with Postman:
- Install [Postman](https://www.getpostman.com/) or any preferred REST API Client such as [Insomnia](https://insomnia.rest/), [Rest Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client), etc.
- Get the application up and running by following the instructions in the Installation Guide of this README.

## Discussion
This section contains justifications and improvements that should be made.

### Compromises
This application is supposed to be completed within four (4) hours; and while this solution is extensive, I will discuss tradeoffs I'd have made if I had to implement this in 4 hours.

#### Structure
The application structure would have been more primitive. The current structure is more domain-driven than anything, following Django's convention as inspiration which works pretty well. This means that lots of abstracted code such as base classes for database and pydantic schemas may have been left out or simply repeated. I would have had the entirety of the endpoints in a single file, database schemas together, same as services and utility functions.

#### Containerization
Perhaps, this is a "me"-thing, but in cases where there are a number of infrastructures needed to make the application work such as the use of Redis and Postgres, I would have focused more on making the application work within a container rather than ensure it had steps for working with it both inside and outside a container

#### Tests and databases
The use of a mock dependency for Postgres in the `conftest.temp_db` would have remained while a mocking of Redis would have been left out since using the same Redis instance would have only resulted in overwriting values rather than throwing contraint exceptions. I'd have also dropped the use of Redis altogether since the database could be used for caching which may be okay at least. The test cases currently are pretty important so I'd have left them in place.

#### Services
It is hard to say if I would have left out the separation of services because while it's the bulk of the application, its presence ensured I wrote functionalities which worked on first run! The focus of type hinting by FastAPI was a very handy feature in this case. So, services would have stayed except it would look uglier and everything would be in a single `services.Service` class.


### Choice of Database
Postgres is used as a database to store information. Seeing that the two tables: `user` and `conversionhistory` are related, it makes sense to use a relational database like PostgreSQL.

I choose Redis for the purpose of caching requests. Since the supported currencies don't change much, it can as well be cached to reduce network calls subsequently. This improves speed of the application.

### Improvements for a production API
- The API for converting amounts is only updated once a day. This means the user is not necessarily getting a real-time information on exchange rates except for the opening prices. It makes sense then, to use a real-time API which is within budget to handle this.

## Licence 🔐
[MIT licensed](/LICENSE) © [Ayodeji Adeoti](https://github.com/Lord-sarcatic)

## Credits 🙏
- Blog posts that helped me get started with FastAPI as this is my first time working with FastAPI

## To do
Add a UI from [Dribble](https://dribbble.com/shots/15090067-Cryptocurrency-Trading-Platform)
