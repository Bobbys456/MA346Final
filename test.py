import pandas as pd
import os

df = pd.read_csv(os.path.join("data",'Senate_lobby_totals_by_year.csv'))

print(df)