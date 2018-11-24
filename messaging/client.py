import paho.mqtt.client as mqtt
from os import environ
# TODO: inject logger instead of binding to flask and fix startup logging
from flask import current_app
from json import dumps as to_json

BROKER_HOST = environ.get('BROKER_HOST')
if not BROKER_HOST:
    raise ValueError('no broker host set')


def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code {}".format(str(rc)))
    current_app.logger.info("Connected with result code {}".format(str(rc)))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


client = mqtt.Client()
client.on_connect = on_connect


def connect():
    current_app.logger.info('connecting to: {}'.format(BROKER_HOST))
    print('connecting to: {}'.format(BROKER_HOST))
    client.connect(BROKER_HOST)
    client.loop_start()


def update_session(name):
    current_app.logger.info("sending update message")

    client.publish('robocars/{}/session'.format('blown302'), to_json({'name': name}))





