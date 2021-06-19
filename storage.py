from redis import from_url
import json
import os

REDIS_URL = os.getenv('REDIS_URL', 'localhost')


def get_locations(user_id):
    conn = from_url(REDIS_URL)
    locations = conn.get(user_id)
    if locations:
        return json.loads(locations)
    else:
        return []


def set_locations(user_id, locations):
    conn = from_url(REDIS_URL)
    locations = conn.set(user_id, json.dumps(locations))


def update_locations(user_id, location):
    locations = get_locations(user_id)
    locations.append(location)
    set_locations(user_id, locations)


def reset_locations(user_id):
    set_locations(user_id, [])
