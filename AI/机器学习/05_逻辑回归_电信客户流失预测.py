import pandas as pd
import numpy as np

def data_preprocess():
  churn_data = pd.read_csv('./data/churn.csv')
  churn_data.info()
  print(churn_data.head(5))
if __name__ == '__main__':
    data_preprocess()