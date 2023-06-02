import pandas as pd
from pandas_profiling import ProfileReport

df = pd.read_csv("cyberbullying_tweets.csv")
print(df)

profile = ProfileReport(df)
profile.to_file(output_file="cyberbullying_report.html")

