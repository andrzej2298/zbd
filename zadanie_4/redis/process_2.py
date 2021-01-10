import sys
import redis
import faker

node_no = sys.argv[1]
channel_input = f"basic_info_{node_no}"
channel_output = f"full_info_{node_no}"
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub(ignore_subscribe_messages=True)
p.subscribe(channel_input)

fake = faker.Faker()

for message in p.listen():
    serial = int(message["data"])
    user = f"users:{serial}"
    country = fake.country().replace("'", "")
    city = fake.city().replace("'", "")
    r.hset(user, "country", country)
    r.hset(user, "city", city)
    r.publish(channel_output, serial)
    print(user, country, city)
