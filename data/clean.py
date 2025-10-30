import pandas as pd

df = pd.read_csv("data/uber-raw-data-apr14.csv")  # ✅ correct relative path
df.columns = ["pickup_datetime", "latitude", "longitude", "base"]
df["passenger_count"] = 1
df.to_csv("uber_sample.csv", index=False)
