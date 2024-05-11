import pandas as pd
import csv

input_file = "random_crawl_src/uni_info.txt"
df = pd.read_csv(input_file, sep=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
columns_to_drops = ["URL", "Total", "Methods"]
df_modified = df.drop(columns=columns_to_drops)

df_modified.to_csv("random_crawl_src/final.csv", index=False)