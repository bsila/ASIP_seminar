# %% - učitavanje knjižnica i konstanti
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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


# %% - funkcija za kreiranje niza 'čistih podataka'
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
                water_level_array.append([date, row[month], row["ID"]])

    # Sortiranje podataka
    water_level_array = sorted(water_level_array, key=lambda x: x[0])

    # Formatiranje datuma
    water_level_array = [
        [date.strftime("%d.%m.%Y"), value, id] for date, value, id in water_level_array
    ]

    return water_level_array


# %% - funkcija za prikaz podataka
def plot_water_levels(water_level_array):
    # Dinamični dohvat postaja
    station_data = pd.DataFrame(water_level_array, columns=["Datum", "Vodostaj", "ID"])
    unique_ids = station_data["ID"].unique()

    plt.figure(figsize=(10, 6))

    for station_id in unique_ids:
        # Filtriranje podataka samo za trenutni
        filtered_data = [row for row in water_level_array if row[2] == station_id]

        # Dohvat datumo i vrijednosti
        dates = [row[0] for row in filtered_data]
        water_levels = [row[1] for row in filtered_data]

        plt.plot(dates, water_levels, label=f"Postaja {station_id}")

    plt.xlabel("Datum")
    plt.ylabel("Vodostaj (m)")
    plt.title("Mjereni vodostaji rijeke Albany")
    plt.legend()

    # Odabir samo ograničenog broja datuma jer se inače prikazuju svi
    dates = station_data["Datum"].unique()
    num_dates = len(dates)
    max_ticks = 10  # Maksimalan broj oznaka na x-osi
    step = max(1, num_dates // max_ticks)  # Korak za oznake na x-osi

    plt.xticks(range(0, num_dates, step), dates[::step], rotation=45)
    plt.grid(True)
    plt.show()


# Funkcija samo za testiranje
def plot_water_levels_for_one_station(water_level_array, station_id):
    # Filtriranje podataka samo za određeni ID postaje
    filtered_data = [row for row in water_level_array if row[2] == station_id]

    # Dohvat datumo i vrijednosti
    dates = [row[0] for row in filtered_data]
    water_levels = [row[1] for row in filtered_data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, water_levels)
    plt.xlabel("Datum")
    plt.ylabel("Vodostaj (m)")
    plt.title(f"Mjereni vodostaji postaje {station_id}")

    # Odabir samo ograničenog broja datuma jer se inače prikazuju svi
    num_dates = len(dates)
    max_ticks = 10  # Maksimalan broj oznaka na x-osi
    step = max(1, num_dates // max_ticks)  # Korak za oznake na x-osi

    plt.xticks(range(0, num_dates, step), dates[::step], rotation=45)
    plt.grid(True)
    plt.show()


# %% - funkcija za korelaciju
def correlate_water_levels(water_level_array):
    water_level_array = pd.DataFrame(
        water_level_array, columns=["Datum", "Vodostaj", "ID"]
    )

    # Pretvorba stupca "Datum" u datetime format
    water_level_array["Datum"] = pd.to_datetime(
        water_level_array["Datum"], format="%d.%m.%Y"
    )

    # Sortiranje podataka po datumu
    water_level_array.sort_values(by="Datum", inplace=True)

    # Grupiranje podataka po ID mjerne postaje
    grouped = water_level_array.groupby("ID")

    # Izračun faznih pomaka za svaku postaju
    fazni_pomak_po_postaji = {}

    for postaja, podaci in grouped:
        fazni_pomak = (
            podaci["Vodostaj"].diff().fillna(0)
        )  # Razlika između trenutnog i prethodnog vodostaja
        fazni_pomak_po_postaji[postaja] = fazni_pomak.to_numpy()

    # Pretvaranje faznih pomaka u DataFrame
    fazni_pomak_df = pd.DataFrame(fazni_pomak_po_postaji)

    # Izračun korelacijske matrice između faznih pomaka
    correlation_matrix = fazni_pomak_df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", linewidths=0.5)
    plt.title("Korelacijska Matrica Faznih Pomaka Mjernih Postaja")
    plt.show()


# %% - učitavanje i obrada podataka
# Učitavanje podataka iz datoteke
data_full = pd.read_csv(f"{data_dir}daily_20230123T1539.csv", skiprows=[0])

# Za testiranje i provjeru podataka korišten manji dataset
# data = pd.read_csv(f"{data_dir}test_set.csv", skiprows=[0])

# Sortiranje podataka po datumu
# !! ORIGINAL datoteka je imala ID napisan kao ' ID' - sa razmakom !!
data_full.sort_values(by=["YEAR", "DD"], inplace=True)
data = data_full[(data_full["PARAM"] == 2)]

# Odabir samo novijih podataka
# Filtriranje podataka za postaju '04HA002', parametar 2 i godine iz 21. stoljeća
filtered_data = data[
    (data["ID"] == "04HA002") & (data["PARAM"] == 2) & (data["YEAR"] >= 2000)
]

# %% - provera postaja
unique_ids = data["ID"].unique()
print(f"Postaje: {unique_ids}")

# %% Odabir samo potrebnih stupaca
selected_columns = [
    "ID",
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

# %% - dohvat čistih podataka
# Za testiranje i provjeru podataka korišten manji dataset
# water_level_array = create_water_level_array(filtered_data)

water_level_array = create_water_level_array(data)


# %% - filtriranje podataka - dohvat samo oni fatuma kada postoje vodostaju za sve postaje
# Pronađite zajedničke datume
def get_valid_dates(water_level_array):
    df = pd.DataFrame(water_level_array, columns=["Datum", "Vodostaj", "ID"])

    df = df.dropna(subset=["Vodostaj"])

    common_dates = set.intersection(
        *[set(df[df["ID"] == station]["Datum"]) for station in df["ID"].unique()]
    )

    # Filtrirajte podatke samo za zajedničke datume
    df = df[df["Datum"].isin(common_dates)]
    water_level_array = df.values

    return water_level_array


# %% - filtriranje datuma
water_level_array = get_valid_dates(water_level_array)

# %% - pozivanje funkcije za prikaz podataka
plot_water_levels(water_level_array)


# %% - pozivanje funkcije za analizu
correlate_water_levels(water_level_array)
