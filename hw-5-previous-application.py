import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import hw_5_feature_count
import warnings
warnings.filterwarnings('ignore')

all_data = pd.read_csv('/kaggle/input/shiftlogs/previous_application.csv')
target = pd.read_csv('/kaggle/input/shiftlogs/application_train.csv')
target = target[['SK_ID_CURR', 'TARGET', 'AMT_INCOME_TOTAL', 'AMT_CREDIT']]

all_data = pd.merge(all_data, target, on="SK_ID_CURR", how="left")
all_data = all_data[all_data['TARGET'].notna()]
all_data = all_data.drop_duplicates(subset=['SK_ID_CURR'])



main(all_data)
