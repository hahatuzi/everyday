# 底部采用打分函数决定是否分支
import joblib
import pandas as pd
# import xgboost as xgb
import numpy as np
from collections import Counter

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.utils._repr_html import estimator


def categray():
  data = pd.read_csv('./data/红酒品质分类.csv')
  x = data.iloc[:, :-1]
  y = data.iloc[:, :-1] - 3
  print(x[:5])
  print(y[:5])

  x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 23, stratify = y)
  #   将测试集特征和标签数据拼接在一起
  pd.concat([x_train,y_train], axis=1).to_csv('./data/红酒分类_train.csv', index = False)
  pd.concat([x_test, y_test], axis=1).to_csv('./data/红酒分类_test.csv', index=False)

def train_modal():
    train_data = pd.read_csv('./data/红酒分类_train.csv')
    test_data = pd.read_csv('./data/红酒分类_test.csv')

    x_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1]

    x_test = test_data.iloc[:, :-1]
    y_test = test_data.iloc[:, -1]

    estimator = xgb.XGBClassifier(
        max_depth = 5,
        n_estimators = 100,
        learning_rate = 0.1,
        random_state = 23,
        objective = 'multi:softmax',
    )
    # 加入平衡权重，因为数据样本不均衡
    class_weight.compute_class_weight('balance', classes=np.unique(y_train), y=y_train)
    estimator.fit(x_train, y_train)
    y_pred = estimator.predict(x_test)
    print(classification.report(y_test, y_pred))
    print(estimator.__best_estimator_)


def use_model():
    train_data = pd.read_csv('./data/红酒分类_train.csv')
    test_data = pd.read_csv('./data/红酒分类_test.csv')

    x_train = train_data.iloc[:, :-1]
    y_train = train_data.iloc[:, -1]

    x_test = test_data.iloc[:, :-1]
    y_test = test_data.iloc[:, -1]

    estimator = joblib.load('./model/xgb_model.pkl')
    # 创建网格分类+交叉验证
    # 定义变量
    param_dict = {
        'n_estimators': [30,50,100,150],
        'max_depth': [2,3,5,6,7],
        'learning_rate': [0.2,0.3,1,1.3],
    }
    #     创建分层采样对象
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=23)
    gs_estimator = GridSearchCV(estimator, param_dict,cv = skf)
    gs_estimator.fit(x_train, y_train)
    gs_y_pred = gs_estimator.predict(x_test)
    print(f'预测值为：{gs_y_pred}')
    print(f'最优评分为：{gs_estimator.best_score_}')
    print(f'准确率为：{accuracy_score(y_test,gs_y_pred)}')

if __name__ == '__main__':
    categray()