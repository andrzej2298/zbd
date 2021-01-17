import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Some example data to display
# x = np.linspace(0, 2 * np.pi, 400)
# y = np.sin(x ** 2)

mpl.style.use("seaborn")
postgres = np.genfromtxt("dane_postgres.csv", delimiter=",")
redis = np.genfromtxt("dane_redis.csv", delimiter=",")

fig, (ax1, ax2) = plt.subplots(1, 2)
fig.suptitle("liczba reklam wyemitowanych przez 30 s")

ax1.plot(postgres[:, 0], postgres[:, 1], marker=".", label="reklamy na czas")
ax1.plot(postgres[:, 0], postgres[:, 2], marker=".", label="reklamy opóźnione")
ax1.set_title("Postgres")
ax1.set_xlabel("liczba uruchomionych grup")
ax1.set_ylim([-10,2500])
ax1.legend(loc="upper left")

ax2.plot(redis[:, 0], redis[:, 1], marker=".", label="reklamy na czas")
ax2.plot(redis[:, 0], redis[:, 2], marker=".", label="reklamy opóźnione")
ax2.set_title("Redis")
ax2.set_xlabel("liczba uruchomionych grup")
ax2.set_ylim([-10,2500])
ax2.legend(loc="upper left")

plt.tight_layout()
plt.savefig("raw_both.png")
