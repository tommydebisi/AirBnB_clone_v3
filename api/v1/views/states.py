#!/usr/bin/python3
""" states module """
from api.v1.views import app_views
from api import storage, State
from flask import jsonify, request
from werkzeug.exceptions import MethodNotAllowed, NotFound, BadRequest

http_methods = ['GET', 'POST', 'PUT', 'DELETE']


@app_views.route('/states', methods=http_methods, strict_slashes=False)
@app_views.route('/states/<state_id>', methods=http_methods,
                 strict_slashes=False)
def state_by_Id(state_id=None):
    """
        Retrieve, delete. create and update State
    """
    methods_dic = {
        'GET': get_state,
        'POST': post_state,
        'PUT': put_state,
        'DELETE': delete_state
    }

    if request.method in methods_dic:
        return methods_dic[request.method](state_id)
    raise MethodNotAllowed(http_methods)


def get_state(state_id=None):
    """
        gets the state object in json format
    """
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            raise NotFound()
        return jsonify(state.to_dict()), 200

    list_states = []
    for obj in storage.all(State).values():
        list_states.append(obj.to_dict())
    return jsonify(list_states)


def delete_state(state_id=None):
    """
        Deletes state object
    """
    if not state_id:
        raise NotFound()

    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def post_state(state_id=None):
    """
        posts to a state object
    """
    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    if not parse_data.get('name'):
        raise BadRequest('Missing name')

    new_state = State(**parse_data)
    return jsonify(new_state.to_dict()), 201


def put_state(state_id=None):
    """
        updates a state
    """
    if not state_id:
        raise NotFound()

    state = storage.get(State, state_id)
    if not state:
        raise NotFound()

    parse_data = request.get_json()
    if type(parse_data) is not dict:
        raise BadRequest('Not a JSON')

    ignore = ['id', 'created_at', 'updated_at']
    for key in parse_data.keys():
        if key not in ignore:
            setattr(state, key, parse_data.get(key))
    state.save()
    return jsonify(state.to_dict()), 200
