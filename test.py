import pandas_profiling
import pandas as pd

df = pd.read_csv('advertising.csv', sep=';')

profile = pandas_profiling.ProfileReport(df)
profile.to_file(outputfile="output.html")
