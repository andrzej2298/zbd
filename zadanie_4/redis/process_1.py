import sys
import redis
import numpy as np
import faker
from time import sleep

node_no = sys.argv[1]
channel = f"basic_info_{node_no}"
r = redis.Redis(host='localhost', port=6379, db=0)

fake = faker.Faker()

while True:
    serial = r.incr("users")
    user = f"users:{serial}"
    cookie = fake.md5()
    ip = fake.ipv4()
    r.hset(user, "user_cookie", cookie)
    r.hset(user, "ip", ip)
    r.publish(channel, serial)
    print(user, cookie, ip)
    sleep(.1)

