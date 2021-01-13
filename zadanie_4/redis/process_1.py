import sys
import redis
import numpy as np
import faker
from datetime import datetime
from time import sleep

node_no = sys.argv[1]
channel = f"basic_info_{node_no}"
r = redis.Redis(host='localhost', port=6379, db=0)

fake = faker.Faker()

while True:
    serial = r.incr("users")
    request = f"requests:{serial}"
    cookie = fake.md5()
    ip = fake.ipv4()
    r.hset(request, "user_cookie", cookie)
    r.hset(request, "ip", ip)
    dt = str(datetime.now())
    r.hset(request, "datetime", dt)
    r.publish(channel, serial)
    print(request, cookie, ip, dt)
    sleep(.1)

