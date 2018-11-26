from os import path, mkdir, listdir
from json import dumps as to_json, loads as to_dic
import pathlib
from glob import glob

DATA_DIRECTORY = '/data/data'
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
    name_sessions = [int(s) for s in get_sessions_by_name(new_name)]
    new_count = max(name_sessions) + 1 if len(name_sessions) != 0 else 1
    with open(SESSIONS_FILE_PATH, 'w') as f:
        f.write(to_json({'name': new_name, 'count': new_count, 'status': 'active'}))

    pathlib.Path(path.join(SESSIONS_DIRECTORY_PATH, new_name, str(new_count))).mkdir(parents=True, exist_ok=True)
    return {'name': new_name, 'count': new_count}


def deactivate_current_session():
    with open(SESSIONS_FILE_PATH, 'r') as f:
        data = to_dic(f.read())

    data['status'] = 'inactive'

    with open(SESSIONS_FILE_PATH, 'w') as f:
        f.write(to_json(data))
    return data


def map_to_session(top_level, sub_level):
    return {
        'name': path.basename(top_level),
        'history': sub_level
    }


def get_sessions():
    return [map_to_session(top_level, listdir(top_level)) for top_level in
            glob(path.join(SESSIONS_DIRECTORY_PATH, '*[!json]'))]


def get_sessions_by_name(name):
    dir_path = path.join(SESSIONS_DIRECTORY_PATH, name)
    if not path.isdir(dir_path):
        return []

    return listdir(dir_path)

