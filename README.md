# Backend API

## Function

- User Registration: user needs to offer first name, last name, desired username, email adress and password
- User Login
- User Logout
- User upload files (to be done)
- User delete files (to be done)
- User download files (to be done)

## Run flask and postgreSQL on docker using following code:

`docker-compose up --build` (if already build, then simply run `docker-compose up`)

## init database (need to improve)

in flask_server run:
`flask db init`
`flask db migrate`
`flask db upgrade`
