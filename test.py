# Predictive Maintenance
from sklearn.linear_model import LogisticRegression
from rpy2 import robjects
import pandas as pd
import numpy as np

file_name = ["cement_mill", "roller_press", "separator", "feeder"]
df = {file:pd.read_csv('/Data' + file + '.csv') for file in file_name}

df1 = pd.merge(df["cement_mill"], df["roller_press"], on='t_stamp')
df2 = pd.merge(df["separator"], df["feeder"], on='t_stamp')
df = pd.merge(df1, df2, on='t_stamp')

# Remove SV and MV Features
df = df[df.columns[~df.columns.str.endswith('sv')]]
df = df[df.columns[~df.columns.str.endswith('mv')]]
print(df)

# Remove Columns with Low Variance

# Replace 0 value as NA

# Label Target by Timestamp
df_target = pd.DataFrame()
df_target['target'] = np.where(df['t_stamp'] > "2017-12-07 00:00:00.000", 1, 0)
df = pd.concat([df, df_target])
print(df)
# Remove Entrie Rows


# Remove Non-operating Machine
# Theshold set to 4000

df = df[df["mill drive_power"] > 4000 ]

# Subtraction (Drive/ Non-Drive) 
gap = df["roller_drive_gap"] - df["roller_nondrive_gap"]
pres = df["roller_drive_pres"] - df["roller_nondrive_pres"]

del df["roller_drive_gap"], df["roller_nondrive_gap"]
del df["roller_drive_pres"], df["roller_nondrive_pres"]

gap = gap.to_frame("roller_gap_diff")
pres = pres.to_frame("roller_pres_diff")
df = df.join(gap)
df = df.join(pres)

# 