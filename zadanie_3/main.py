import psycopg2
import psycopg2.extras
import psycopg2.errors
import numpy as np
import faker
import faker.config
from enum import Enum, auto
from collections import OrderedDict
from multiprocessing import Pool
from pprint import pprint
from time import sleep

DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"
MAX_CANDIES = 500
ELVES_COUNT = 20
SINGLE_ELF_PRESENTS = 100
MAX_CANDIES_IN_PRESENT = 10
MAX_CANDIES_TO_PICK = 10
MAX_SIMILAR_CANDIES = 10


class Status:
    SUCCESS = "SUCCESS"
    DEADLOCK = "DEADLOCK"
    CHECK_VIOLATION = "CHECK_VIOLATION"
    SYNTAX_ERROR = "SYNTAX_ERROR"


def add_candies(candies, cur):
    result = []
    for candy in candies:
        candy_count = np.random.randint(MAX_CANDIES)
        candy = candy.replace("'", "").replace("\n", "")
        cur.execute(f"insert into slodycz_w_magazynie values ('{candy}', '{candy_count}')")
        result.append(candy)
    return result


def add_present_contents(candies, serial, cur):
    candies_for_person = np.random.randint(1, MAX_CANDIES_IN_PRESENT)
    chosen_candy = np.random.choice(candies, size=candies_for_person, replace=False)
    result = []

    for candy in chosen_candy:
        chosen_quantity = np.random.randint(1, MAX_CANDIES_TO_PICK)
        cur.execute(f"insert into slodycz_w_paczce"
                    f" values ({serial}, '{candy}', {chosen_quantity})")
        result.append((serial, candy, chosen_quantity))
    return result


def add_similarities(candies, cur):
    for candy in candies:
        similar_candy_count = np.random.randint(MAX_SIMILAR_CANDIES)
        similar_candies = [c for c in np.random.choice(candies, size=similar_candy_count) if c != candy]
        similarities = np.random.uniform(size=similar_candy_count)
        for (similar_candy, similarity) in zip(similar_candies, similarities):
            cur.execute(f"insert into podobny_slodycz values ('{candy}', '{similar_candy}', {similarity})")


def prepare_database():
    with open("candies.txt") as candies, open("prepare_database.sql") as prepare_file, \
         psycopg2.connect(DATABASE_SETUP) as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(prepare_file.read())
        candies = add_candies(candies, cur)
        add_similarities(candies, cur)

        return candies


def run_elf(assignment):
    (worker_no, candy_names) = assignment
    with psycopg2.connect(DATABASE_SETUP) as conn:
        fake = faker.Faker(OrderedDict((locale, 1) for locale in faker.config.AVAILABLE_LOCALES))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        chosen_nationalities = np.random.choice(faker.config.AVAILABLE_LOCALES, SINGLE_ELF_PRESENTS)
        results = []

        for nationality in chosen_nationalities:
            name = fake[nationality].name()
            country = nationality

            results.append(ship_one_present(candy_names, country, cur, name, results))

        return results


def ship_one_present(candy_names, country, cur, name, result):
    cur.execute("begin")

    # defining the present
    cur.execute(f"insert into paczka (kraj, opis_obdarowanego)"
                f" values ('{country}', '{name}')"
                f" returning identyfikator")
    serial = cur.fetchone()["identyfikator"]
    result.append((serial, country, name))
    candies = add_present_contents(candy_names, serial, cur)

    for (serial, candy, chosen_quantity) in candies:
        try:
            if not fetch_one_candy(candy, chosen_quantity, cur):
                substitute_found = False
                cur.execute(f"select ktory_slodycz_jest_podobny"
                            f" from podobny_slodycz"
                            f" where do_czego_slodycz_jest_podobny = '{candy}'"
                            f" order by podobienstwo desc")
                substitutes = cur.fetchall()
                for substitute in substitutes:
                    substitute_candy = substitute["ktory_slodycz_jest_podobny"]
                    substitute_found = fetch_one_candy(substitute_candy, chosen_quantity, cur)
                    if substitute_found:
                        break
                if not substitute_found:
                    cur.execute("rollback")
                    return Status.CHECK_VIOLATION
        except psycopg2.errors.DeadlockDetected:
            cur.execute("rollback")
            return Status.DEADLOCK
        except psycopg2.errors.SyntaxError:
            cur.execute("rollback")
            return Status.SYNTAX_ERROR
        except psycopg2.errors.CheckViolation:
            cur.execute("rollback")
            return Status.CHECK_VIOLATION

    cur.execute("commit")
    return Status.SUCCESS


def fetch_one_candy(candy, chosen_quantity, cur):
    cur.execute(f"select ilosc_pozostalych"
                f" from slodycz_w_magazynie"
                f" where nazwa = '{candy}'")
    remaining = cur.fetchone()["ilosc_pozostalych"]
    if remaining >= chosen_quantity:
        cur.execute(f"update slodycz_w_magazynie"
                    f" set ilosc_pozostalych = ilosc_pozostalych - {chosen_quantity}"
                    f" where nazwa = '{candy}'")
        return True
    else:
        return False


if __name__ == "__main__":
    all_candies = prepare_database()
    elf_assignments = [(i, all_candies) for i in range(ELVES_COUNT)]
    with Pool(ELVES_COUNT) as p:
        pprint(p.map(run_elf, elf_assignments))
