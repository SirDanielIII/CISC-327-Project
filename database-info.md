# Database Information

This app utilizes Flask-SQLAlchemy and Flask-Migrate as an ORM around a sqlite database.

## Flask-SQLAlchemy

This library provides the bulk of the functionality required by the app.
It is used for creating database tables based on models, handling all interactions with the database.
This approach was chosen as it offers the most flexibility and ease of use allowing all group members to
utilize the models as needed.

## Flask-Migrate

This library is used to easily create database migrations based on model updates in the python code.
The migrations are then applied to the database on application startup.
They can also be applied manually beforehand by running this command from the app directory.

```shell
flask db upgrade
```

### Model Developers

After changing any models run the following command to create a new migration:

```shell
flask db migrate -m "Migration Name Here"
```
