import pandas as pd
import numpy as np

df = pd.read_excel(file_path, header=None)
df.columns = ["time", "volume"]

df = df[pd.to_datetime(df["time"], errors="coerce").notna()]
df["time"] = pd.to_datetime(df["time"])
df["volume"] = pd.to_numeric(df["volume"], errors="coerce").fillna(0)

df["date"] = df["time"].dt.date
df["bucket"] = df["time"].dt.strftime("%H:%M")

daily = df.groupby("date")["volume"].sum()
daily = daily[daily > 0]

df = df[df["date"].isin(daily.index)]
df = df.merge(daily.rename("daily_total"), on="date")
df["pct"] = df["volume"] / df["daily_total"]

profile = df.groupby("bucket")["pct"].median().reset_index()
profile["bucket_dt"] = pd.to_datetime(profile["bucket"], format="%H:%M")
profile = profile.sort_values("bucket_dt")

profile["pct_smooth"] = profile["pct"].rolling(3, center=True, min_periods=1).mean()
profile["pct_final"] = profile["pct_smooth"] / profile["pct_smooth"].sum()
profile["cum_pct"] = profile["pct_final"].cumsum()

profile.head(), profile.tail(), profile["pct_final"].sum()
