#!/usr/bin/python3
"""
    Users module
"""
from api.v1.views import app_views
from api import storage, User
from flask import jsonify, request
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest


http_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/users', methods=http_methods,
                 strict_slashes=False)
@app_views.route('/users/<user_id>', methods=http_methods,
                 strict_slashes=False)
def user_by_Id(user_id=None):
    """
        Retrieve, delete. create and update city
    """
    methods_dic = {
        'GET': get_user,
        'POST': post_user,
        'PUT': put_user,
        'DELETE': delete_user
    }

    if request.method in methods_dic:
        return methods_dic[request.method](user_id)
    raise MethodNotAllowed(http_methods)


def get_user(user_id=None):
    """
        gets the city object in json format
    """
    if user_id:
        userr = storage.get(User, user_id)
        if not userr:
            raise NotFound()
        return jsonify(userr.to_dict()), 200

    user_objs = list(map(lambda x: x.to_dict(),
                     storage.all(User).values()))
    return jsonify(user_objs)


def delete_user(user_id=None):
    """
        Deletes user object
    """
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def post_user(user_id=None):
    """
        posts to a user object
    """
    if not storage.get(User, user_id):
        raise NotFound()

    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    if not parse_data.get('email'):
        raise BadRequest('Missing email')

    if not parse_data.get('password'):
        raise BadRequest('Missing password')

    new_user = User(**parse_data)
    return jsonify(new_user.to_dict()), 201


def put_user(user_id=None):
    """
        updates a user
    """
    if user_id:
        userr = storage.get(User, user_id)
        if userr:
            parse_data = request.get_json()
            if type(parse_data) is not dict:
                raise BadRequest('Not a JSON')

            ignore = ['id', 'created_at', 'updated_at', 'email']
            for key, val in parse_data.items():
                if key not in ignore:
                    setattr(userr, key, val)
            userr.save()
            return jsonify(userr.to_dict()), 200
    raise NotFound()
