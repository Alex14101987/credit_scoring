import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
import matplotlib.pyplot as plt
import hw_5_feature_count
import warnings
warnings.filterwarnings('ignore')

train = pd.read_csv('/kaggle/input/shiftlogs/application_train.csv')
test = pd.read_csv('/kaggle/input/shiftlogs/application_test.csv')

all_data = pd.concat((train, test)).reset_index(drop=True)

main(all_data)

