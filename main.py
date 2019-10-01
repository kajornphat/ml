# Predictive Maintenance
from rpy2 import robjects
import pandas as pd
import numpy as np

from rpy2.robjects import pandas2ri
from rpy2.robjects import default_converter
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.lib.dplyr import DataFrame

def convert_df(dataframe):      
    '''Convert between 
    Pandas dataframe to R "Dataframe"'''
    with localconverter(default_converter + pandas2ri.converter) as cv:
        try:
                dataframe = pandas2ri.ri2py(dataframe)
        except:
                dataframe = DataFrame(dataframe)
    return dataframe

r = robjects.r

# Data Preperation
file_name = ["cement_mill", "roller_press", "separator", "feeder"]
df = {file:pd.read_csv('Data/' + file + '.csv') for file in file_name}

df1 = pd.merge(df["cement_mill"], df["roller_press"], on='t_stamp')
df2 = pd.merge(df["separator"], df["feeder"], on='t_stamp')
df = pd.merge(df1, df2, on='t_stamp')

### Remove SV and MV Features
df = df[df.columns[~df.columns.str.endswith('sv')]]
df = df[df.columns[~df.columns.str.endswith('mv')]]

r.assign('dataset', convert_df(df))
r('''

library(caret)
library(dplyr)

bad_cols <- nearZeroVar(dataset)
dataset <- dataset[, -bad_cols]

dataset[dataset == 0] <- NA

dataset["target"] <- ifelse(dataset$t_stamp >= "2017-12-07", 1, 0)

dataset <- dataset %>%
    filter(get("mill.drive_power") > 4000)

''')
df = convert_df(r('dataset'))

for i in df:
    # Count no. NaN in columns
    no_Nan = df[i].isna().sum()
    no_col = df[i].shape[0]
    percent = (no_Nan/no_col) * 100
    if percent >= 10:
        df = df.drop(columns=i)
#     print("{:.2f}% Missing in Columns {}".format(percent, i))

# Remove row
df = df.dropna()

# Subtraction (Drive/ Non-Drive) 
gap = df["roller_drive_gap"] - df["roller_nondrive_gap"]
pres = df["roller_drive_pres"] - df["roller_nondrive_pres"]

del df["roller_drive_gap"], df["roller_nondrive_gap"]
del df["roller_drive_pres"], df["roller_nondrive_pres"]

gap = gap.to_frame("roller_gap_diff")
pres = pres.to_frame("roller_pres_diff")
df = df.join(gap)
df = df.join(pres)