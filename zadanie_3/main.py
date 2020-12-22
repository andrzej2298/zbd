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
from typing import List, Tuple


ELVES_COUNT = 20
DATABASE_SETUP = "dbname=database" \
                 " user=root" \
                 " host=127.0.0.1" \
                 " password=password"


class IsolationLevel(Enum):
    SERIALIZABLE = "serializable"
    REPEATABLE_READ = "repeatable read"
    READ_COMMITTED = "read committed"


class Settings(BaseModel):
    MAX_CANDIES: int
    SINGLE_ELF_PRESENTS: int
    MAX_CANDIES_IN_PRESENT: int
    MAX_CANDIES_TO_PICK: int
    MAX_SIMILAR_CANDIES: int
    ISOLATION_LEVEL: IsolationLevel
    ADVERSARIES: int


class Status(Enum):
    SUCCESS = "SUCCESS"
    DEADLOCK = "DEADLOCK"
    CHECK_VIOLATION = "CHECK_VIOLATION"
    SERIALIZATION_FAILURE = "SERIALIZATION_FAILURE"
    SYNTAX_ERROR = "SYNTAX_ERROR"


def add_candies(candies, cur, settings: Settings):
    result = []
    for candy in candies:
        candy_count = np.random.randint(settings.MAX_CANDIES)
        candy = candy.replace("'", "").replace("\n", "")
        cur.execute(f"insert into slodycz_w_magazynie values ('{candy}', '{candy_count}')")
        result.append(candy)
    return result


def add_present_contents(candies, serial, cur, settings: Settings):
    candies_for_person = np.random.randint(1, settings.MAX_CANDIES_IN_PRESENT)
    chosen_candy = np.random.choice(candies, size=candies_for_person, replace=False)
    result = []

    for candy in chosen_candy:
        chosen_quantity = np.random.randint(1, settings.MAX_CANDIES_TO_PICK)
        cur.execute(f"insert into slodycz_w_paczce"
                    f" values ({serial}, '{candy}', {chosen_quantity})")
        result.append((serial, candy, chosen_quantity))
    return result


def add_similarities(candies, cur, settings: Settings):
    for candy in candies:
        similar_candy_count = np.random.randint(settings.MAX_SIMILAR_CANDIES)
        similar_candies = [c for c in np.random.choice(candies, size=similar_candy_count) if c != candy]
        similarities = np.random.uniform(size=similar_candy_count)
        for (similar_candy, similarity) in zip(similar_candies, similarities):
            cur.execute(f"insert into podobny_slodycz values ('{candy}', '{similar_candy}', {similarity})")


def prepare_database(settings: Settings):
    with open("candies.txt") as candies, open("prepare_database.sql") as prepare_file, \
         psycopg2.connect(DATABASE_SETUP) as conn:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(prepare_file.read())
        candies = add_candies(candies, cur, settings)
        add_similarities(candies, cur, settings)

        return candies


def run_elf(assignment):
    (worker_no, candy_names, settings) = assignment

    print(f"elf {worker_no} starts")
    with psycopg2.connect(DATABASE_SETUP) as conn:
        fake = faker.Faker(OrderedDict((locale, 1) for locale in faker.config.AVAILABLE_LOCALES))
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        chosen_nationalities = np.random.choice(faker.config.AVAILABLE_LOCALES, settings.SINGLE_ELF_PRESENTS)
        results = []

        for nationality in chosen_nationalities:
            name = fake[nationality].name().replace("'", "")
            country = nationality

            results.append(ship_one_present(candy_names, country, cur, settings, name, worker_no))

        print(f"elf {worker_no} ends")
        return results


def ship_one_present(candy_names, country, cur, settings, name, worker_no) -> Status:
    cur.execute(f"begin isolation level {settings.ISOLATION_LEVEL.value}")
    # defining the present
    cur.execute(f"insert into paczka (kraj, opis_obdarowanego)"
                f" values ('{country}', '{name}')"
                f" returning identyfikator")
    serial = cur.fetchone()["identyfikator"]
    try:
        candies = add_present_contents(candy_names, serial, cur, settings)
        for (serial, candy, chosen_quantity) in candies:
            if not fetch_one_candy(candy, chosen_quantity, cur, settings, worker_no):
                substitute_found = False
                cur.execute(f"select ktory_slodycz_jest_podobny"
                            f" from podobny_slodycz"
                            f" where do_czego_slodycz_jest_podobny = '{candy}'"
                            f" order by podobienstwo desc")
                substitutes = cur.fetchall()
                for substitute in substitutes:
                    substitute_candy = substitute["ktory_slodycz_jest_podobny"]
                    substitute_found = fetch_one_candy(substitute_candy, chosen_quantity, cur, settings, worker_no)
                    if substitute_found:
                        break
                if not substitute_found:
                    cur.execute("rollback")
                    return Status.CHECK_VIOLATION
        cur.execute("commit")
    except psycopg2.errors.DeadlockDetected:
        cur.execute("rollback")
        return Status.DEADLOCK
    except psycopg2.errors.SyntaxError:
        cur.execute("rollback")
        return Status.SYNTAX_ERROR
    except psycopg2.errors.CheckViolation:
        cur.execute("rollback")
        return Status.CHECK_VIOLATION
    except psycopg2.errors.SerializationFailure:
        cur.execute("rollback")
        return Status.SERIALIZATION_FAILURE
    else:
        return Status.SUCCESS


def fetch_one_candy(candy, chosen_quantity, cur, settings: Settings, worker_no):
    cur.execute(f"select ilosc_pozostalych"
                f" from slodycz_w_magazynie"
                f" where nazwa = '{candy}'")
    is_adversary = worker_no < settings.ADVERSARIES
    remaining = cur.fetchone()["ilosc_pozostalych"]
    if remaining >= chosen_quantity:
        if is_adversary:
            cur.execute("select sum(numbackends) from pg_stat_database")
            ongoing_transactions = cur.fetchone()["sum"]
            if ongoing_transactions > 1 + settings.ADVERSARIES:
                print("adversary sleeps")
                sleep(5)
        cur.execute(f"update slodycz_w_magazynie"
                    f" set ilosc_pozostalych = ilosc_pozostalych - {chosen_quantity}"
                    f" where nazwa = '{candy}'")
        return True
    else:
        return False


if __name__ == "__main__":
    figure_no = 1
    sns.set_theme()
    transactions_per_second_columns = []
    transactions_per_second_data = []
    failed_transactions = []
    # for (isolation_level, max_candies) in [(IsolationLevel.SERIALIZABLE, 500)]:
    for (isolation_level, max_candies, adversaries) in itertools.product([IsolationLevel.SERIALIZABLE], [1000], list(range(5))):
    # for (isolation_level, max_candies, adversaries) in itertools.product(IsolationLevel, [1000], list(range(5))):
        factory_settings = Settings(
            MAX_CANDIES=max_candies,
            SINGLE_ELF_PRESENTS=100,
            MAX_CANDIES_IN_PRESENT=10,
            MAX_CANDIES_TO_PICK=10,
            MAX_SIMILAR_CANDIES=10,
            ISOLATION_LEVEL=isolation_level,
            ADVERSARIES=adversaries,
        )
        experiment_name = f"{isolation_level.value.replace(' ', '_')}" \
                          f"_{factory_settings.MAX_CANDIES}" \
                          f"_a{adversaries}"
        print(f"start {experiment_name}")
        all_candies = prepare_database(factory_settings)
        elf_assignments = [(i, all_candies, factory_settings) for i in range(ELVES_COUNT)]
        time_before = datetime.now()
        with Pool(ELVES_COUNT) as p:
            current_results: List[List[Status]] = p.map(run_elf, elf_assignments)
        time_after = datetime.now()
        global_time = (time_after - time_before).total_seconds()

        present_statuses: List[Status] = []

        for elf_result in current_results:
            for present_status in elf_result:
                present_statuses.append(present_status)

        succeeded_transactions = len(list(filter(lambda x: x == Status.SUCCESS, present_statuses)))
        transactions_per_second = succeeded_transactions / global_time
        transactions_per_second_data.append(transactions_per_second)
        transactions_per_second_columns.append(experiment_name)
        failed_transactions.append(len(present_statuses) - succeeded_transactions)
        print(transactions_per_second)
        statuses: List[Status] = list(Status)
        status_counts: List[int] = []
        for status in statuses:
            status_counts.append(len([i for i in present_statuses if str(i) == str(status)]))
        data = {
            "status": list(map(lambda x: x.value, statuses)),
            "count": status_counts,
        }
        df = pd.DataFrame(data)
        print(data)
        print(df)

        plt.figure(figure_no)
        figure_no += 1
        ax = sns.barplot(x="status", y="count", data=data)
        ax.set_title(f"isolation level: {isolation_level.value.upper()}")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
        plt.tight_layout()
        plot_file_name = f"statuses_{experiment_name}.png"
        csv_file_name = f"statuses_{experiment_name}.csv"
        df.to_csv(csv_file_name)
        plt.savefig(plot_file_name)
    transactions_data = {
        "experiment": transactions_per_second_columns,
        "transactions_per_second": transactions_per_second_data,
        "failed_transactions": failed_transactions,
    }
    transactions_df = pd.DataFrame(transactions_data)
    print(transactions_data)
    print(transactions_df)
    transactions_df.to_csv("transactions_per_second.csv")
