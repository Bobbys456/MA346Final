import pandas as pd

df = pd.read_csv('data/data.csv')

df['URL'].to_csv("data/raw_links.csv")