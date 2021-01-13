import sys
import redis
import faker
import numpy as np
from enum import Enum, auto
from cachetools import LRUCache
from datetime import datetime
from datetime import timedelta


class Choices(Enum):
    EMIT_1 = auto()
    EMIT_12 = auto()
    NO_EMIT = auto()


def what_to_do() -> Choices:
    return np.random.choice(list(Choices), p=[.1, .6, .3])

def emit(serial: int, request: str, r: redis.Redis) -> None:
    serial = r.incr("emissions")
    emission = f"emissions:{serial}"
    r.set(emission, "true")
    request_time = datetime.fromisoformat(r.hget(request, "datetime").decode())
    ms_delta = (datetime.now() - request_time) / timedelta(milliseconds=1)
    delayed_ad = ms_delta > 20


fake = faker.Faker()
node_no = sys.argv[1]
channel_input_basic = f"basic_info_{node_no}"
channel_input_full = f"full_info_{node_no}"
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe(channel_input_basic, channel_input_full)
cache = LRUCache(100000)

for message in p.listen():
    serial = int(message["data"])
    request = f"requests:{serial}"
    channel = message["channel"].decode()
    choice: Choices
    if serial in cache:
        choice = cache[serial]
    else:
        choice = what_to_do()
    print(request, choice)
    if (channel == channel_input_basic and choice == Choices.EMIT_1 or
        channel == channel_input_full and choice == Choices.EMIT_12):
        emit(serial, request, r)
