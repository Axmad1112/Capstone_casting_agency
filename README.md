
# FSND-Casting-Agency

Udacity Full Stack Nanodegree capstone project - casting_agency


# Motivation

This project is the capstone project for Udacity Full Stack web development Nanondegree.

This project covers all the learnt concepts that were covered by the nanodegree which includes data modeling for web using postgres, API development and testing with Flask, Authorization with RBAC, JWT authentication and finally API deployment using Heroku.

# Start the project locally

This section will introduce you to how to run and setup the app locally.

# Dependencies

This project is based on Python and Flask.

To install project dependencies:

bash
$ pip install -r requirements.txt

Note: you must have the latest version of Python

# Local Database connection

- You need to install and start postgres database.
- You need to update the database_params variable found in config.py file as shown below:

python
database_param = {
    "username": "postgres",
    "password": "DB_PASSWORD",
    "db_name": "casting_agency",
    "dialect": "postgresql"
}

Note: you can create a db named casting_agency by using createdb command as shown below:

bash
createdb -U postgres casting_agency

# Auth0 configs

You need to update auth0_params variable found in config.py with auth0 configurations

python

AUTH0_DOMAIN = 'casting-agency1112.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Casting_agency'



# Run the app locally

You can run the app using the below commands:

bash

set FLASK_APP=app.py
flask run

# Run test cases

You can run the unit test cases that are defined in test_app.py using the below command:

bash

python test_app.py

# API Documentation

This section will introduce you to API endpoints and error handling


# Error handling

Errors are returned as JSON in the following format:

json
{
    "success": False,
    "error": 403,
    "message": "Foribdden"
}

The API will return the types of errors:

- 400 – bad request
- 401 - Unauthorized
- 403 - Foribdden
- 404 – Not Found. Resource Not found or Web page doesn't exist
- 405 - Method Not Allowed
- 422 – Unprocessable Entity. An error occured while processing your request
- 500 - internal server error


# API Endpoints

This API supports two types of resources /actors and /movies. Each resource support four HTTP methods; GET, POST, PATCH, DELETE


# GET /actors

- General: returns a list of all actors
- Sample request:

bash
curl -X GET http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"

- Sample response:

json
{
  "actors": [
    { "age": 25, "gender": "Male", "id": 1, "name": "Ahmad" },
    { "age": 22, "gender": "Male", "id": 2, "name": "Boburbek" },
    { "age": 23, "gender": "Female", "id": 3, "name": "Feruza" }
  ],
  "success": true
}

# GET /movies

- General: returns a list of all movies
- Sample request:

bash
curl -X GET http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"

- Sample response:

json
{
  "movies": [
    {
      "actors": ["Ahmad", "Boburbek"],
      "id": 1,
      "release_date": "Mon, 28 March 2005 00:00:00 GMT",
      "title": "Prison break"
    },
    {
      "actors": ["Feruza"],
      "id": 2,
      "release_date": "Mon, 15 Jun 2020 00:00:00 GMT",
      "title": "Women"
    }
  ],
  "success": true
}

# POST /actors

- General: create a new actor
- Sample request:

bash
curl -X POST http://127.0.0.1:5000/actors -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN"  -d '{"name" : "Umar", "age" : "24", "gender":"Male"}'

- Sample response: <i>returns the new actor id</i>

json
{ "created": 4, "success": true }

# POST /movies

- General: create a new movie
- Sample request:

bash
curl -X POST http://127.0.0.1:5000/movies -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"title" : "Uzuklar hukmdori", "release_date" : "5/7/2010"}'

- Sample response: <i>returns the new movie id</i>

json
{ "created": 3, "success": true }

# PATCH /actors/\<int:actor_id\>

- General: update an existing actor
- Sample request:
  <i>you can update actor's name, gender and age</i>

bash
curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"name" : "Ahmad Togayev"}'

- Sample response: <i>returns the updated actor object</i>

json
{
  "actor": { "age": 28, "gender": "Male", "id": 1, "name": "Ahmad Togayev" },
  "success": true
}

# PATCH /movies/\<int:movie_id\>

- General: update an existing movie
- Sample request:
  <i>you can update movies's title and release date</i>

bash
curl -X PATCH http://127.0.0.1:5000/movies/1 -H "Content-Type: application/json" -H "Authorization: Bearer ACCESS_TOKEN" -d '{"title" : "movie_title", "release_date" : "8/4/2015"
}'

- Sample response: <i>returns the updated movie object which includes the actors acting in this movie</i>

json
{
  "movie": {
    "actors": ["Ahmad Togayev", "Umar"],
    "id": 1,
    "release_date": "Mon, 23 Jun 2018 00:00:00 GMT",
    "title": "movie_name"
  },
  "success": true
}

# DELETE /actors/\<int:actor_id\>

- General: delete an existing actor
- Sample request:

bash
curl -X DELETE http://127.0.0.1:5000/actors/1 -H "Authorization: Bearer ACCESS_TOKEN"

- Sample response: <i>returns the deleted actor id</i>

json
{ "Delete occured": 1, "success": true }

# DELETE /movies/\<int:movie_id\>

- General: delete an existing movie
- Sample request:

bash
curl -X DELETE http://127.0.0.1:5000/movies/1 -H "Authorization: Bearer ACCESS_TOKEN"

- Sample response: <i>returns the deleted movie id</i>

json
{ "Delete occured": 1, "success": true }



# Authentication and authorization


[Auth0 Applications](https://auth0.com/docs/applications)
<br>
[Auth0 APIs](https://auth0.com/docs/api/info)

# Existing user roles



1. Casting Assistant:

- GET /actors (get:actors): can get all actors
- GET /movies (get:movies): can get all movies

2. Casting Director:
- All permissions of Casting Assistant
- POST /actors (create:actors): can create new actors
- PATCH /actors (update:actors): can update existing actors
- PATCH /movies (update:movies): can update existing movies
- DELETE /actors (delete:actors): can delete actors from database

3. Exectutive Director:
- All permissions of Casting Director
- POST /movies (create:movies): Can create new movies
- DELETE /movies (delete:movies): Can delete movies from database