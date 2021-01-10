import select
import sys

import psycopg2
import psycopg2.extras
import psycopg2.extensions
import faker

DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"


node_no = sys.argv[1]
fake = faker.Faker()
conn = psycopg2.connect(DATABASE_SETUP)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
channel = f"basic_info_{node_no}"
cur.execute(f"LISTEN {channel}")

print(f"Waiting for notifications on channel '{channel}'")
while True:
    if select.select([conn], [], []) == ([], [], []):
        print("Timeout")
    else:
        conn.poll()
        while conn.notifies:
            notify = conn.notifies.pop(0)

            serial = int(notify.payload)
            country = fake.country().replace("'", "")
            city = fake.city().replace("'", "")
            query = f"insert into user_info values ({serial}, '{country}', '{city}')"
            cur.execute(query)

            notification = f"notify full_info_{node_no}, '{serial}'"
            cur.execute(notification)

            print(query)
