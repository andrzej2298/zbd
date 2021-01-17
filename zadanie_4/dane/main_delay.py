import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.style.use("seaborn")
postgres = np.genfromtxt("dane_postgres_delay.csv", delimiter=",")
redis = np.genfromtxt("dane_redis_delay.csv", delimiter=",")

postgres_sorted = postgres[postgres[:, 1].argsort()]
redis_sorted = redis[redis[:, 1].argsort()]

fig, ax = plt.subplots(4, 2)
# fig.suptitle("liczba reklam wyemitowanych przez 30 s")

for i in range(4):
        # row = 4*i + j
    postgres_data = postgres_sorted[(4*i):(4*i+4), :]
    redis_data = redis_sorted[(4*i):(4*i+4), :]
    print(postgres_data)
    print(redis_data)
    ms_delay = int(postgres_data[0, 1])
    ax[i][0].plot(postgres_data[:, 0], postgres_data[:, 2], marker=".", label="na czas")
    ax[i][0].plot(postgres_data[:, 0], postgres_data[:, 3], marker=".", label="opóźnione")
    ax[i][0].set_title(f"Postgres, {ms_delay} ms obliczeń")
    ax[i][0].set_xlabel("liczba uruchomionych grup")
    ax[i][0].set_ylim([0,2500])
    # ax[i][0].legend(loc="upper left")
    ax[i][1].plot(redis_data[:, 0], redis_data[:, 2], marker=".", label="na czas")
    ax[i][1].plot(redis_data[:, 0], redis_data[:, 3], marker=".", label="opóźnione")
    ax[i][1].set_title(f"Redis, {ms_delay} ms obliczeń")
    ax[i][1].set_xlabel("liczba uruchomionych grup")
    ax[i][1].set_ylim([0,2500])
    # ax[i][1].legend(loc="upper left")

handles, labels = ax[3][1].get_legend_handles_labels()
fig.set_figheight(10)
fig.legend(handles, labels, loc='upper center', framealpha=1, facecolor="white")

plt.tight_layout()
plt.savefig("raw_both_delay.png")
