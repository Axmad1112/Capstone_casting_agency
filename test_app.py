import unittest
import os
from models import db, Movie, Actor
from config import database_param
import jwt_value
from models import db, setup_db
from app import app
import json


database_path = "{}://{}:{}@localhost:5432/{}".format(
    database_param["dialect"],
    database_param["username"],
    database_param["password"],
    database_param["db_name"])

casting_assistant = jwt_value.casting_assistant
casting_director = jwt_value.casting_director
executive_producer = jwt_value.executive_producer


def set_auth_header(role):
    if role == 'assistant':
        return {"Authorization": f"Bearer {casting_assistant}"}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(casting_director)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(executive_producer)}


class MainTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.database_path = database_path
        self.db = setup_db(self.app, self.database_path)
        self.db.create_all()
        self.movie_data = {
            "title": "title",
            "release_date": "2020.04.12"
        }
        self.bad_data = {
            "title": "",
            "release_date": ""
        }
        self.actor_data = {
            "name": "Ahmad",
            "gender": "Male",
            "age": 25
        }
    # movies endpoint tests

    def tearDown(self):
        " Execute after all tests"
        pass

    def test_get_movies(self):
        res = self.client.get(
            '/actors', headers={
                "Authorization": f"Bearer {casting_assistant}"})
        self.assertEqual(res.status_code, 200)

    def test_add_movie(self):
        res = self.client.post(
            '/movies', json=self.movie_data,
            headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_movie_fail(self):
        res = self.client.post(
            '/movies', json={}, headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_add_movie_forbidden(self):
        res = self.client.post(
            '/movies', json=self.movie_data,
            headers=set_auth_header('assistant'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data["success"], False)

    def test_edit_movie(self):
        movie_id = Movie.query.all()[0]
        res = self.client.patch(f'/movies/{movie_id.id}', json=self.movie_data,
                                headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_movie_forbidden(self):

        movie_id = Movie.query.first().id
        res = self.client.patch(
            f'/movies/{movie_id}', json=self.movie_data,
            headers=set_auth_header('assistant'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_delete_movie(self):
        movie_id = Movie.query.all()[-1]  # eng oxirgi element
        res = self.client.delete(
            f'/movies/{movie_id.id}',
            headers=set_auth_header('producer'))  # data jo'natmaymiz
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_forbidden(self):
        movie = Movie.query.all()[-1]
        res = self.client.delete(
            f'/movies/{movie.id}',
            headers=set_auth_header('director'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    # actors endpoint tests

    def test_get_actors(self):
        res = self.client.get(
            '/actors', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_actors_unauthorized(self):
        res = self.client.get(
            '/actors', headers=set_auth_header(''))
        self.assertEqual(res.status_code, 401)

    def test_add_actor(self):
        res = self.client.post(
            '/actors', json=self.actor_data,
            headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_actor_fail(self):
        res = self.client.post(
            '/actors', json={}, headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_add_actor_forbidden(self):
        res = self.client.post(
            '/actors', json=self.actor_data,
            headers=set_auth_header('assistant'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_edit_actor(self):
        actor_id = Actor.query.first().id
        res = self.client.patch(
            f'/actors/{actor_id}', json=self.actor_data,
            headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_actor_forbidden(self):
        actor_id = Actor.query.first().id
        res = self.client.patch(
            f'/actors/{actor_id}', json=self.actor_data,
            headers=set_auth_header('assistant'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_edit_actor_fail(self):
        actor_id = Actor.query.first().id
        res = self.client.patch(
            f'/actors/{actor_id}', data={},
            headers=set_auth_header('assistant'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)

    def test_delete_actor(self):
        actor = Actor.query.all()[-1]
        res = self.client.delete(
            f'/actors/{actor.id}',
            headers=set_auth_header('producer'))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_forbidden(self):
        actor = Actor.query.all()[-1]
        res = self.client.delete(
            f'/actors/{actor.id}',
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()
