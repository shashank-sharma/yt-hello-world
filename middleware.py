from functools import wraps
from flask import request, jsonify, abort, make_response


def is_required(parameters=None, files=None):
    """
    Check what is required for any given Flask API Endpoint (GET/POST)
    :param parameters: Possible parameters required for given API request
    :param files: Files required for given API request
    :return:
    """

    def actual_decorator(func):
        @wraps(func)
        def newFunc(*args, **kwargs):
            if request.method == 'GET':
                request_param = request.args
                for i in parameters:
                    if i not in request_param:
                        abort(make_response(jsonify(message="Parameter " + i + " not found"), 400))
                    if not request_param.get(i):
                        abort(make_response(jsonify(message="Invalid value for " + i), 400))
            else:
                request_json = request.json
                request_files = request.files

                if parameters:
                    if not request_json:
                        abort(make_response(jsonify(message="Invalid Request"), 400))
                    for i in parameters:
                        if i not in request_json:
                            abort(make_response(jsonify(message="Parameter " + i + " not found"), 400))
                        if not request_json[i]:
                            abort(make_response(jsonify(message="Invalid value for " + i), 400))
                if files:
                    if not request_files:
                        abort(make_response(jsonify(message="Invalid Request"), 400))
                    for i in files:
                        if i not in request_files:
                            if i not in request_files:
                                abort(make_response(jsonify(message="File " + i + " not found"), 400))
            return func(*args, **kwargs)

        return newFunc

    return actual_decorator
