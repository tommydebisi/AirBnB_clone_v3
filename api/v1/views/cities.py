#!/usr/bin/python3
"""
    cities module
"""
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest
from api.v1.views import app_views
from api import storage, State, City, storage_t
from flask import jsonify, request


http_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/states/<state_id>/cities', methods=http_methods,
                 strict_slashes=False)
@app_views.route('/cities/<city_id>', methods=http_methods,
                 strict_slashes=False)
def city_by_Id(city_id=None, state_id=None):
    """
        Retrieve, delete. create and update city
    """
    methods_dic = {
        'GET': get_city,
        'POST': post_city,
        'PUT': put_city,
        'DELETE': delete_city
    }

    if request.method in methods_dic:
        return methods_dic[request.method](city_id, state_id)
    raise MethodNotAllowed(http_methods)


def get_city(city_id=None, state_id=None):
    """
        gets the city object in json format
    """
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            raise NotFound()
        city_objs = list(map(lambda x: x.to_dict(), state.cities))
        return jsonify(city_objs), 200

    city = storage.get(City, city_id)
    if not city:
        raise NotFound()
    return jsonify(city.to_dict())


def delete_city(city_id=None, state_id=None):
    """
        Deletes city object
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)

        if storage_t == 'db':
            for place in storage.all(Place).values():
                if place.city_id == city_id:
                    for review in storage.all(Review).values():
                        if review.place_id == place.id:
                            storage.delete(review)
                    storage.delete(place)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def post_city(city_id=None, state_id=None):
    """
        posts to a city object
    """
    if not storage.get(State, state_id):
        raise NotFound()

    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    if not parse_data.get('name'):
        raise BadRequest('Missing name')

    new_city = City(**parse_data)
    return jsonify(new_city.to_dict()), 201


def put_city(city_id=None, state_id=None):
    """
        updates a city
    """
    if city_id:
        city = storage.get(City, city_id)
        if city:
            parse_data = request.get_json()
            if type(parse_data) is not dict:
                raise BadRequest('Not a JSON')

            ignore = ['id', 'created_at', 'updated_at', 'state_id']
            for key, val in parse_data.items():
                if key not in ignore:
                    setattr(city, key, val)
            city.save()
            return jsonify(city.to_dict()), 200
    raise NotFound()
