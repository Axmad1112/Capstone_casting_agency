import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, db_drop_and_create_all, \
    Actor, Movie, db

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app) 



    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, PUT, POST,DELETE, OPTIONS')
        return response

    @app.route('/')
    def index():
        return jsonify({
            "success": True,
            "message": "Hello, Udacity team!"
        })
                                
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def retrieve_actors(self):
        actors_all = Actor.query.order_by(Actor.id).all()
        actors = [actor.get_format_json() for actor in actors_all]

        return jsonify({
            'success': True,
            'actors': actors
        }), 200



    # POST /actors create a new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actors')
    def create_new_actor(jwt):
        data = request.get_json()
        name = data.get('name',  None)
        age = data.get('age', None)
        gender = data.get('gender', None)
        movie_id = data.get('movie_id', None)
        if data and name and age and gender:
            actor = Actor(name=name, age=age, gender=gender)
            if movie_id:
                try:
                    movie_id = int(movie_id)
                    actor.movie_id = movie_id
                except ValueError: abort(400)
            actor.insert()
            new_actor = Actor.query.get(actor.id)

            return jsonify({
                'success': True,
                'created': actor.id,
                'new_actor': new_actor.get_format_json()
            })
        else:
            abort(400)

    # PATCH /actors/<id> update an actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(self, actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)
        body = request.get_json()
        age = body.get('age', None)
        name = body.get('name', None)
        gender = body.get('gender', None)
        movie_id = body.get('movie_id', None)

        try:
            if name is not None:
                actor.name = name
            if age is not None:
                actor.age = age
            if gender is not None:
                actor.gender = gender
            if movie_id is not None:
                actor.movie_id = movie_id

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.get_format_json()
            }), 200

        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()


    # Delete /actors/<id> delete an actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(self, actor_id):
        # Actor.query.filter(Actor.id == actor_id).delete() o'zgartiramiz
        actor = Actor.query.get_or_404(actor_id)
        try:
            actor.delete()
        except:
            abort(422)
        finally:
            db.session.close()
        return jsonify({
            "success": True,
            "message" : "Delete occured"
        })


    # GET /movies get movies with their actors endpoint
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def retrieve_movies(self):
        movies_all = Movie.query.order_by(Movie.id).all()
        
        movies = [movie.format() for movie in movies_all]

        # if len(movies) == 0:
        #     abort(404)

        return jsonify({
            'success': True,
            'movies': movies
        }), 200


    # POST /movies create a new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movies')
    def create_movie(self):
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)


        if (title is None) or (release_date is None):
            abort(400)
        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            new_movie = Movie.query.get(movie.id)
            
            return jsonify({
                'success': True,
                'created': movie.id,
                'new_movie':new_movie.format()
            }), 200

        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()

    # PATCH /movies/<id> update a movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)

        # if movie is None:
        #     abort(404)
        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)

        if title is not None:
            movie.title = title
        if release_date is not None:
            movie.release_date = release_date

        movie.update()

        return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

        #     db.session.rollback()
        #     abort(422)
        # finally:
        #     db.session.close()


    # Delete /movies/<id> delete a movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(self, movie_id):
        movie = Movie.query.get_or_404(movie_id)
        try: movie.delete()
        except: abort(422)
        finally:
            db.session.close()
        return jsonify({
            "success": True,
            "message" : "Delete occured"
        })

    # Health check endpoint
    @app.route('/health-check', methods=['POST', 'GET'])
    def health_check():
        return jsonify("Health Check for the API")


    # error handler for AuthError
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    # Error Handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": """Bad Request. The request may be
            incorrect or corrupted"""
        }), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return {
            "success": False,
            "error_code": 401,
            "error_message": "Unauthorized"
        }, 401

    @app.errorhandler(403)
    def foribdden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Foribdden"
        }), 403
        
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": """Not Found. Resource Not found or
            Web page doesn't exist"""
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": """Unprocessable Entity.
            An error occured while processing your request"""
        }), 422

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error Occured"
        }), 500

    return app


app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)