#!/usr/bin/python3
"""
    Place_reviews module
"""
from api.v1.views import app_views
from api import storage, Place, Review, User
from flask import jsonify, request
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest


http_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/cities/<place_id>/reviews', methods=http_methods,
                 strict_slashes=False)
@app_views.route('/reviews/<review_id>', methods=http_methods,
                 strict_slashes=False)
def review_by_Id(place_id=None, review_id=None):
    """
        Retrieve, delete. create and update city
    """
    methods_dic = {
        'GET': get_review,
        'POST': post_review,
        'PUT': put_review,
        'DELETE': delete_review
    }

    if request.method in methods_dic:
        return methods_dic[request.method](place_id, review_id)
    raise MethodNotAllowed(http_methods)


def get_review(place_id=None, review_id=None):
    """
        gets the review object in json format
    """

    if review_id:
        revieww = storage.get(Review, review_id)
        if not revieww:
            raise NotFound()
        return jsonify(revieww.to_dict()), 200

    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    place_objs = list(map(lambda x: x.to_dict(), place.reviews))
    return jsonify(place_objs), 200


def delete_review(place_id=None, review_id=None):
    """
        Deletes review object
    """
    revieww = storage.get(Review, review_id)
    if revieww:
        storage.delete(revieww)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def post_review(place_id=None, review_id=None):
    """
        posts to a review object
    """
    if not storage.get(Place, place_id):
        raise NotFound()

    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    if not (user_id := parse_data.get('user_id')):
        raise BadRequest('Missing user_id')

    if not storage.get(User, user_id):
        raise NotFound()

    if not parse_data.get('text'):
        raise BadRequest('Missing text')

    new_review = Review(**parse_data)
    return jsonify(new_review.to_dict()), 201


def put_review(place_id=None, review_id=None):
    """
        updates review
    """
    if review_id:
        revieww = storage.get(Review, review_id)
        if revieww:
            parse_data = request.get_json()
            if type(parse_data) is not dict:
                raise BadRequest('Not a JSON')

            ignore = ['id', 'created_at', 'updated_at', 'user_id', 'place_id']
            for key, val in parse_data.items():
                if key not in ignore:
                    setattr(revieww, key, val)
            revieww.save()
            return jsonify(revieww.to_dict()), 200
    raise NotFound()
