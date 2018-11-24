from flask import Flask, jsonify, request
import logging
import messaging.client as client
import repositories.data as data_access


def create_app():
    app = Flask(__name__)

    with app.app_context():
        client.connect()
        app.logger.setLevel(logging.DEBUG)

    return app


app = create_app()


@app.route('/sessions', methods=['GET', 'POST'])
def sessions():
    if request.method == 'GET':
        return jsonify(get_sessions())
    elif request.method == 'POST':
        sess = create_session(request.get_json())
        return jsonify("")


def create_session(data):
    app.logger.info('received session request: {}'.format(data))
    data_access.create_session(data['name'])
    client.update_session(data['name'])


def get_sessions():
    return data_access.get_sessions()


if __name__ == '__main__':
    data_access.init()
    app.run(debug=True, host='0.0.0.0')
