from sklearn.datasets import load_boston
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import Ridge,RidgeCV

import pandas as pd
import numpy as np

data_url = 'http://lib.stat.cmu.edu/datasets/boston'