from os import path, mkdir, listdir
from json import dumps as to_json

DATA_DIRECTORY = '/app/data'
SESSIONS_DIRECTORY = 'sessions'
SESSIONS_DIRECTORY_PATH = path.join(DATA_DIRECTORY, SESSIONS_DIRECTORY)
SESSIONS_FILE_PATH = path.join(SESSIONS_DIRECTORY_PATH, 'sessions.json')


def init():
    if not path.isdir(DATA_DIRECTORY):
        mkdir(DATA_DIRECTORY)
    if not path.isdir(SESSIONS_DIRECTORY_PATH):
        mkdir(SESSIONS_DIRECTORY_PATH)
    if not path.exists(SESSIONS_FILE_PATH):
        with open(SESSIONS_FILE_PATH, 'w') as f:
            f.write(to_json({'name': None}))


def create_session(new_name):
    max_count = 0
    for s in get_sessions():

        existing_name, str_count = s.split('::')

        if existing_name == new_name:
            count = int(str_count)
            if max_count < count:
                max_count = count

    new_count = max_count + 1
    with open(SESSIONS_FILE_PATH, 'w') as f:
        f.write(to_json({'name': new_name, 'count': new_count}))

    mkdir('{}/{}::{}'.format(SESSIONS_DIRECTORY_PATH, new_name, new_count))


def get_sessions():
    return [dI for dI in listdir(SESSIONS_DIRECTORY_PATH) if not path.splitext(dI)[1]]





