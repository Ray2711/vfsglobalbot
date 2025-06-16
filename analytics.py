import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

CSV_PATH = "appointments.csv"

def load_data(path=CSV_PATH):
    # читаем CSV, парсим даты
    df = pd.read_csv(
        path,
        names=["scraped_at", "city", "available_date"],
        parse_dates=["scraped_at", "available_date"],
        dtype={"city": str}
    )
    return df

def filter_data(df, start_date, end_date, city):
    mask = (
        (df["scraped_at"].dt.date >= start_date.date()) &
        (df["scraped_at"].dt.date <= end_date.date()) &
        (df["city"].str.lower() == city.lower())
    )
    return df.loc[mask]

def plot_counts(df_filtered, city, start_date, end_date):
    # группируем по дате скрейпа и считаем кол-во доступных записей
    counts = df_filtered.groupby(df_filtered["scraped_at"].dt.date).size()
    plt.figure(figsize=(10, 5))
    counts.plot(marker="o", linestyle="-")
    plt.title(f"Доступные даты для «{city}»\nс {start_date.date()} по {end_date.date()}")
    plt.xlabel("Дата сканирования")
    plt.ylabel("Число найденных дат")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    df = load_data()

    # интерактивный ввод
    s = input("Дата от (YYYY-MM-DD): ").strip()
    e = input("Дата до (YYYY-MM-DD): ").strip()
    city = input("Город/страна: ").strip()

    try:
        start_date = datetime.fromisoformat(s)
        end_date   = datetime.fromisoformat(e)
    except ValueError:
        print("Неверный формат даты. Используйте YYYY-MM-DD.")
        return

    df_filt = filter_data(df, start_date, end_date, city)
    if df_filt.empty:
        print("По заданным параметрам нет данных.")
    else:
        plot_counts(df_filt, city, start_date, end_date)

if __name__ == "__main__":
    main()




    