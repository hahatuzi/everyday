from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge,RidgeCV

import pandas as pd
import numpy as np
# 1.加载波士顿房价数据
data_url = 'http://lib.stat.cmu.edu/datasets/boston'
raw_df = pd.read_csv(data_url, sep='\\s+',skiprows=2,header=None)
data = np.hstack([raw_df.values[::2, :], raw_df.values[1::2, :2]])
target = raw_df.values[1::2, 2]

print(f'特征：{data.shape}')
print(f'特征：{target.shape}')
print(f'特征数据：{data[:5]}')
print(f'特征数据：{target[:5]}')
