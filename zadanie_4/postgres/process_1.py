import select
import sys
import psycopg2
import psycopg2.extras
import psycopg2.extensions
import numpy as np
import faker
from time import sleep

DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"


node_no = sys.argv[1]
channel = f"basic_info_{node_no}"
conn = psycopg2.connect(DATABASE_SETUP)
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

fake = faker.Faker()

while True:
    user_cookie = fake.md5()
    cur.execute(f"insert into user_ad_requests (cookie, ip) values ('{user_cookie}', '{fake.ipv4()}' :: inet) returning id")
    serial = cur.fetchone()["id"]
    query = f"notify {channel}, '{serial}'"
    print(query)
    cur.execute(query)
    print("sleep")
    sleep(0.1)

