#!/usr/bin/python3
"""
    Amenities module
"""
from api.v1.views import app_views
from api import storage, Amenity
from flask import jsonify, request
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest


http_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/amenities', methods=http_methods,
                 strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=http_methods,
                 strict_slashes=False)
def amenity_by_Id(amenity_id=None):
    """
        Retrieve, delete. create and update city
    """
    methods_dic = {
        'GET': get_amenity,
        'POST': post_amenity,
        'PUT': put_amenity,
        'DELETE': delete_amenity
    }

    if request.method in methods_dic:
        return methods_dic[request.method](amenity_id)
    raise MethodNotAllowed(http_methods)


def get_amenity(amenity_id=None):
    """
        gets the city object in json format
    """
    if amenity_id:
        amenityy = storage.get(Amenity, amenity_id)
        if not amenityy:
            raise NotFound()
        return jsonify(amenityy.to_dict()), 200

    amenity_objs = list(map(lambda x: x.to_dict(),
                        storage.all(Amenity).values()))
    return jsonify(amenity_objs)


def delete_amenity(amenity_id=None):
    """
        Deletes amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def post_amenity(amenity_id=None):
    """
        posts to a amenity object
    """
    if not storage.get(Amenity, amenity_id):
        raise NotFound()

    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    if not parse_data.get('name'):
        raise BadRequest('Missing name')

    new_amenity = Amenity(**parse_data)
    return jsonify(new_amenity.to_dict()), 201


def put_amenity(amenity_id=None):
    """
        updates a amenity
    """
    if amenity_id:
        amenityy = storage.get(Amenity, amenity_id)
        if amenityy:
            parse_data = request.get_json()
            if type(parse_data) is not dict:
                raise BadRequest('Not a JSON')

            ignore = ['id', 'created_at', 'updated_at']
            for key, val in parse_data.items():
                if key not in ignore:
                    setattr(amenityy, key, val)
            amenityy.save()
            return jsonify(amenityy.to_dict()), 200
    raise NotFound()
