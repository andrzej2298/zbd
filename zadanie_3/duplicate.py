import itertools
from collections import OrderedDict
from datetime import datetime
from enum import Enum
from multiprocessing import Pool
from time import sleep

import faker
import faker.config
import matplotlib.pyplot as plt
import numpy as np
import psycopg2
import psycopg2.errors
import psycopg2.extras
import seaborn as sns
import pandas as pd
from pydantic import BaseModel
from typing import List, Tuple, Literal

ELVES_COUNT = 20
DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"


with psycopg2.connect(DATABASE_SETUP) as conn:
    fake = faker.Faker(OrderedDict((locale, 1) for locale in faker.config.AVAILABLE_LOCALES))
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("set idle_in_transaction_session_timeout = 1000")
    cur.execute("begin")
    sleep(10)
    cur.execute("commit")
