import select
import sys

import psycopg2
import psycopg2.extras
import psycopg2.extensions
import faker
import numpy as np
from enum import Enum, auto

DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"

class Choices(Enum):
    EMIT_1 = auto()
    EMIT_12 = auto()
    NO_EMIT = auto()


node_no = sys.argv[1]
fake = faker.Faker()
conn = psycopg2.connect(DATABASE_SETUP)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
channel_1 = f"basic_info_{node_no}"
channel_2 = f"full_info_{node_no}"
cur.execute(f"LISTEN {channel_1}")
cur.execute(f"LISTEN {channel_2}")

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
            choice = np.random.choice(list(Choices), p=[.1, .6, .3])
            print(f"choice: {choice}")

            if notify.channel == channel_1:
                print(f"channel 1: {serial}")
            else:
                print(f"channel 2: {serial}")
