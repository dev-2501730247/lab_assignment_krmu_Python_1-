import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# function to take all csv files and join them
def load_all_data():
    data_path = Path("data")

    print("Searching in:", data_path.resolve())
    files = list(data_path.glob("*.csv"))

    if len(files) == 0:
        print("No CSV files found")
        return pd.DataFrame()

    all_dfs = []

    for f in files:
        try:
            temp = pd.read_csv(f)

            # checking if required columns exist
            if "timestamp" not in temp.columns or "kwh" not in temp.columns:
                print("Skipping", f.name, "(missing columns)")
                continue

            temp["Building"] = f.stem        # file name as building name
            temp["timestamp"] = pd.to_datetime(temp["timestamp"])
            all_dfs.append(temp)

        except Exception as e:
            print("Cannot read", f.name, "->", e)

    if len(all_dfs) == 0:
        print("Nothing to combine")
        return pd.DataFrame()

    final = pd.concat(all_dfs, ignore_index=True)
    return final


def calculate_daily_totals(df):
    df = df.set_index("timestamp")
    return df["kwh"].resample("D").sum()


def calculate_weekly_totals(df):
    df = df.set_index("timestamp")
    return df["kwh"].resample("W").sum()


def building_summary(df):
    # simple stats of each building
    return df.groupby("Building")["kwh"].agg(
        mean="mean",
        min="min",
        max="max",
        sum="sum"
    )


# classes for OOP part
class MeterReading:
    def __init__(self, time, units):
        self.timestamp = time
        self.kwh = units


class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add(self, reading):
        self.readings.append(reading)

    def get_total(self):
        return sum(x.kwh for x in self.readings)


class BuildingManager:
    def __init__(self):
        self.all = {}

    def get_or_make(self, name):
        if name not in self.all:
            self.all[name] = Building(name)
        return self.all[name]

    def load_data(self, df):
        for _, row in df.iterrows():
            b = self.get_or_make(row["Building"])
            r = MeterReading(row["timestamp"], row["kwh"])
            b.add(r)

    def whole_campus_usage(self):
        return sum(b.get_total() for b in self.all.values())


# graph/dashboard
def create_dashboard(df, daily, weekly):
    fig, ax = plt.subplots(3, 1, figsize=(10, 12))

    # daily line graph
    ax[0].plot(daily.index, daily.values)
    ax[0].set_title("Daily Energy Usage")
    ax[0].set_ylabel("kWh")

    # avg weekly per building
    df2 = df.set_index("timestamp")
    weekly_avg = (
        df2.groupby("Building")["kwh"]
            .resample("W")
            .sum()
            .groupby("Building")
            .mean()
    )

    ax[1].bar(weekly_avg.index, weekly_avg.values)
    ax[1].set_title("Average Weekly Use (Each Building)")
    ax[1].tick_params(axis="x", rotation=40)

    # scatter for hourly usage
    hourly = df2["kwh"].resample("H").sum()
    ax[2].scatter(hourly.index, hourly.values, s=6)
    ax[2].set_title("Hourly Load (All Buildings)")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    plt.close()


def save_outputs(df, summary, daily, weekly):
    df.to_csv("cleaned_energy_data.csv", index=False)
    summary.to_csv("building_summary.csv")

    total = df["kwh"].sum()
    top = summary["sum"].idxmax()
    peak_row = df.loc[df["kwh"].idxmax()]

    with open("summary.txt", "w") as f:
        f.write(f"Total campus usage: {total:.2f} kWh\n")
        f.write(f"Building with highest usage: {top}\n")
        f.write(f"Peak usage time: {peak_row['timestamp']}\n")


def main():
    df = load_all_data()

    if df.empty:
        print("Nothing loaded, ending program.")
        return

    daily = calculate_daily_totals(df.copy())
    weekly = calculate_weekly_totals(df.copy())
    summary = building_summary(df.copy())

    # OOP manager work
    mgr = BuildingManager()
    mgr.load_data(df.copy())
    print("Total campus use (OOP):", mgr.whole_campus_usage())

    create_dashboard(df.copy(), daily, weekly)
    save_outputs(df.copy(), summary, daily, weekly)


if __name__ == "__main__":
    main()
