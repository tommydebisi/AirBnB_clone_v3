#!/usr/bin/python3
"""
    places module
"""
from api.v1.views import app_views
from api import storage, Place, City, User
from flask import jsonify, request
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest


http_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/cities/<city_id>/places', methods=http_methods,
                 strict_slashes=False)
@app_views.route('/places/<place_id>', methods=http_methods,
                 strict_slashes=False)
def places_by_Id(place_id=None, city_id=None):
    """
        Retrieve, delete. create and update city
    """
    methods_dic = {
        'GET': get_place,
        'POST': post_place,
        'PUT': put_place,
        'DELETE': delete_place
    }

    if request.method in methods_dic:
        return methods_dic[request.method](place_id, city_id)
    raise MethodNotAllowed(http_methods)


def get_place(place_id=None, city_id=None):
    """
        gets the place object in json format
    """

    if place_id:
        placee = storage.get(Place, place_id)
        if not placee:
            raise NotFound()
        return jsonify(placee.to_dict()), 200

    city = storage.get(City, city_id)
    if not city:
        raise NotFound()
    city_objs = list(map(lambda x: x.to_dict(), city.places))
    return jsonify(city_objs), 200


def delete_place(place_id=None, city_id=None):
    """
        Deletes place object
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def post_place(place_id=None, city_id=None):
    """
        posts to a place object
    """
    if not storage.get(City, city_id):
        raise NotFound()

    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    if not (user_id := parse_data.get('user_id')):
        raise BadRequest('Missing user_id')

    if not storage.get(User, user_id):
        raise NotFound()

    if not parse_data.get('name'):
        raise BadRequest('Missing name')

    parse_data.update({'city_id': city_id})
    new_place = Place(**parse_data)
    return jsonify(new_place.to_dict()), 201


def put_place(place_id=None, city_id=None):
    """
        updates place
    """
    if place_id:
        placee = storage.get(Place, place_id)
        if placee:
            parse_data = request.get_json()
            if type(parse_data) is not dict:
                raise BadRequest('Not a JSON')

            ignore = ['id', 'created_at', 'updated_at', 'user_id', 'city_id']
            for key, val in parse_data.items():
                if key not in ignore:
                    setattr(placee, key, val)
            placee.save()
            return jsonify(placee.to_dict()), 200
    raise NotFound()
