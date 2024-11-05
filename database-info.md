# Database Information

This app uses a sqlite3 database in the `app/database` directory called `rent_management.db` and will
create it on intialization if it does not already exist.
Since it is a sqlite3 database, the structure and data can be viewed and modified with any sqlite database browser.
To simply delete all of the data in the database, stop the app, delete the `rent_management.db` file
and on the next startup, a fresh database will be created.

To implement this functionality, this app utilizes Flask-SQLAlchemy and Flask-Migrate as an ORM around a sqlite database.

## Flask-SQLAlchemy

This library provides the bulk of the functionality required by the app.
It is used for creating database tables based on models, handling all interactions with the database.
This approach was chosen as it offers the most flexibility and ease of use allowing all group members to
utilize the models as needed.
Queries can be built with python directly in a control and utilize types easily.
Updates are as as simple as updating the object and then calling save on the db.

## Flask-Migrate

This library is used to easily create database migrations based on model updates in the python code.
The migrations are then applied to the database on application startup.
They can also be applied manually beforehand by running this command from the app directory.

```shell
flask db upgrade
```

### Model Developers

After changing any models run the following command from the app directory to create a new migration:

```shell
flask db migrate -m "Migration Name Here"
```
