import pandas as pd
import os

df = pd.read_csv(os.path.join("data","output.csv"))

df = df[df['text'].notna()]

print(df)

