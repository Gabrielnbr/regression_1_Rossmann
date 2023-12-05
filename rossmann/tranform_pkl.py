import math
import pickle
import numpy                as np
import pandas               as pd
import datetime
import inflection
from Rossmann_copy import Rossmann



pipe = Rossmann()

store = pd.read_csv('data_set/store.csv')
train = pd.read_csv('data_set/train.csv')
df_raw = pd.merge( train, store, how='left', on='Store')

print(df_raw.columns)

data = pipe.data_clenning(df_raw)
print('fim data_clenning')
data1 = pipe.feature_engineering(data)
print('fim feature_engineering')

data1.to_csv('treino.csv', index=False)