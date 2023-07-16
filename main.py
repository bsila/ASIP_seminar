# %% - učitavanje knjižnica i constanti
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

data_dir = "podaci/"


# %%
def create_water_level_array(data):
    water_level_array = []

    # Prikupljanje datuma i vrijednosti vodostaja
    for i, (_, row) in enumerate(data.iterrows()):
        for month in months:
            date = pd.to_datetime(
                f"{int(row['DD'])}.{month}.{int(row['YEAR'])}",
                format="%d.%b.%Y",
                errors="coerce",
            )
            if pd.notnull(date):
                water_level_array.append([date, row[month]])

    # Sortiranje podataka
    water_level_array = sorted(water_level_array, key=lambda x: x[0])

    # Formatiranje datuma
    water_level_array = [
        [date.strftime("%d.%m.%Y"), value] for date, value in water_level_array
    ]

    return water_level_array


# %% - Učitavanje i obrada podataka
# Učitavanje podataka iz datoteke
data = pd.read_csv(f"{data_dir}daily_20230123T1539.csv", skiprows=[0])

# Za testiranje i provjeru podataka korišten manji dataset
# data = pd.read_csv(f"{data_dir}test_set.csv", skiprows=[0])

# Sortiranje podataka po datumu
# !! ORIGINAL datoteka je imala ID napisan kao ' ID' - sa razmakom !!
data.sort_values(by=["YEAR", "DD"], inplace=True)
data = data[(data["ID"] == "04HA002") & (data["PARAM"] == 2)]

# Odabir samo novijih podataka
# Filtriranje podataka za postaju '04HA002', parametar 2 i godine iz 21. stoljeća
filtered_data = data[
    (data["ID"] == "04HA002") & (data["PARAM"] == 2) & (data["YEAR"] >= 2000)
]

# Odabir samo potrebnih stupaca
selected_columns = [
    "YEAR",
    "DD",
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
data = data[selected_columns]
filtered_data = filtered_data[selected_columns]

# %%
# Za testiranje i provjeru podataka korišten manji dataset
# water_level_array = create_water_level_array(filtered_data)

# Vodostaji (PARAM == 2) su dani samo za godine 2010+
water_level_array = create_water_level_array(data)


# %% - Prikaz podataka
def plot_water_levels(water_level_array):
    dates = [row[0] for row in water_level_array]
    water_levels = [row[1] for row in water_level_array]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, water_levels)
    plt.xlabel("Datum")
    plt.ylabel("Vodostaj (m)")
    plt.title("Mjereni vodostaji rijeke Albany")

    # Odabir samo ograničenog broja datuma na x-osi jer se inaće prikazuju svi
    num_dates = len(dates)
    max_ticks = 10  # Maksimalan broj oznaka na x-osi
    step = max(1, num_dates // max_ticks)  # Korak za oznake na x-osi

    plt.xticks(range(0, num_dates, step), dates[::step], rotation=45)
    plt.grid(True)
    plt.show()


# %% - Pozivanje funkcije za prikaz podataka
plot_water_levels(water_level_array)
