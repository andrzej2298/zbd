import select
import sys

import psycopg2
import psycopg2.extras
import psycopg2.extensions
import faker
import numpy as np
from enum import Enum, auto
from cachetools import LRUCache
from datetime import datetime
from datetime import timedelta

DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"

class Choices(Enum):
    EMIT_1 = auto()
    EMIT_12 = auto()
    NO_EMIT = auto()


def emit(serial: int, cur) -> None:
    cur.execute(f"insert into emissions (request_id) values ({serial})")
    cur.execute(f"select dt from user_ad_requests where id={serial}")
    request_time = cur.fetchone()["dt"]
    ms_delta = (datetime.now() - request_time) / timedelta(milliseconds=1)
    if ms_delta > 20:
        cur.execute(f"insert into emissions_delayed (emission_id) values ({serial})")
    else:
        cur.execute(f"insert into emissions_on_time (emission_id) values ({serial})")



node_no = sys.argv[1]
fake = faker.Faker()
conn = psycopg2.connect(DATABASE_SETUP)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
channel_1 = f"basic_info_{node_no}"
channel_2 = f"full_info_{node_no}"
cur.execute(f"LISTEN {channel_1}")
cur.execute(f"LISTEN {channel_2}")
cache = LRUCache(100000)

print(f"Waiting for notifications on channel '{channel_1}'")
print(f"Waiting for notifications on channel '{channel_2}'")
while True:
    if select.select([conn], [], []) == ([], [], []):
        print("Timeout")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)
            serial = int(notify.payload)
            choice: Choices

            if serial in cache:
                choice = cache[serial]
            else:
                choice = np.random.choice(list(Choices), p=[.1, .6, .3])

            if (notify.channel == channel_1 and choice == Choices.EMIT_1 or
                notify.channel == channel_2 and choice == Choices.EMIT_12):
                print("emit")
                emit(serial, cur)
            else:
                print("no emit")
