import sys
import redis
import faker
import numpy as np
from enum import Enum, auto
from cachetools import LRUCache
from datetime import datetime
from datetime import timedelta
from time import sleep


class Choices(Enum):
    EMIT_1 = auto()
    EMIT_12 = auto()
    NO_EMIT = auto()


def emit(serial: int, request: str, r: redis.Redis, sleep_ms: int) -> None:
    sleep(sleep_ms * 0.001)
    serial = r.incr("emissions")
    emission = f"emissions:{serial}"
    r.set(emission, "true")
    request_time = datetime.fromisoformat(r.hget(request, "datetime").decode())
    ms_delta = (datetime.now() - request_time) / timedelta(milliseconds=1)
    if ms_delta > 20:
        r.incr("delayed")
    else:
        r.incr("on_time")


fake = faker.Faker()
node_no = sys.argv[1]
sleep_ms = int(sys.argv[2])
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
        choice = np.random.choice(list(Choices), p=[.1, .6, .3])
    print(request, choice)
    if (channel == channel_input_basic and choice == Choices.EMIT_1 or
        channel == channel_input_full and choice == Choices.EMIT_12):
        emit(serial, request, r, sleep_ms)
