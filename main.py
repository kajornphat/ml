# Predictive Maintenance
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Gather Filename
file_name = ["cement_mill", "roller_press", "separator", "feeder"]
df = {file:pd.read_csv(file + '.csv') for file in file_name}

df1 = pd.merge(df["cement_mill"], df["roller_press"], on='t_stamp')
df2 = pd.merge(df["separator"], df["feeder"], on='t_stamp')
df = pd.merge(df1, df2, on='t_stamp')
