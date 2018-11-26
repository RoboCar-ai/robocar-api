from flask import Flask, jsonify, request
import logging
import messaging.client as client
import repositories.data as data_access
from werkzeug.exceptions import BadRequest, MethodNotAllowed
import traceback


def create_app():
    app = Flask(__name__)

    with app.app_context():
        client.connect()
        app.logger.setLevel(logging.DEBUG)

    return app


app = create_app()


@app.route('/sessions', methods=['GET', 'POST'])
def sessions_handler():
    if request.method == 'GET':
        return jsonify(get_sessions())
    elif request.method == 'POST':
        body = request.get_json()
        if not body.get('status'):
            raise BadRequest('missing status')
        sess = create_session(body)
        return jsonify(sess)
    else:
        raise MethodNotAllowed()


# Delegates
def create_session(data):
    if data['status'] == 'active':
        sess = data_access.create_session(data['name'])
    else:
        sess = data_access.deactivate_current_session()
    client.update_session(data['name'], data['status'])
    return sess


def get_sessions():
    return data_access.get_sessions()


# Error handlers
@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return e.description, e.code


@app.errorhandler(Exception)
def handle_internal_server_error(e):
    traceback.print_exc()
    return str(e), 500


if __name__ == '__main__':
    data_access.init()
    app.run(debug=True, host='0.0.0.0')
