#!/usr/bin/python3
"""
    index module
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def view_app():
    """
        use of flask blueprint to return 'ok' message
    """
    return jsonify(status='ok')


@app_views.route('/stats', strict_slashes=False)
def obj_counts():
    """
        count of all the objects
    """
    from api import Amenity, City, Place, Review, storage, State, User

    count_dic = dict()
    count_dic['amenities'] = storage.count(Amenity)
    count_dic['cities'] = storage.count(City)
    count_dic['places'] = storage.count(Place)
    count_dic['reviews'] = storage.count(Review)
    count_dic['states'] = storage.count(State)
    count_dic['users'] = storage.count(User)

    return jsonify(count_dic)
