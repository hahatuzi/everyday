# GBDT
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report


# 1.加载数据
data = pd.read_csv('./data/titannic.csv')
data.info()
# 2.数据预处理
# 2.1 选择特征和标签

x = data[['Pclass','Sex','Age']]
y = data['Survived']

# 2.2 数据处理
x = x.copy()
# 处理age列的缺失值，用该列的均值填充
x['Age'] = x['Age'].fillna(x['Age'].mean())
# 2.3 热编码处理
x = pd.get_dummies(x, columns=['Sex'])
# print(x)
# print(y)
# 2.4 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size= 0.2,random_state=23)

# 4.模型训练
## 4.1 决策树
estimator1 = DecisionTreeClassifier()
estimator1.fit(x_train, y_train)
## 模型预测
y_pred = estimator1.predict(x_test)
# print(f'决策树的预测结果1为：{estimator1.score(x_test, y_test)}')
print(f'决策树的预测精度为：{accuracy_score(y_test, y_pred)}')
# print(f'分类评估报告\n{classification_report(y_test, y_pred)}')

## 4.2 GBDT
estimator2 = GradientBoostingClassifier()
estimator2.fit(x_train, y_train)
y_pred2 = estimator2.predict(x_test)
print(f'GBDT的预测精度为：{accuracy_score(y_test, y_pred2)}')

## 4.3 基于GBDT进行参数调优
param_dict  = {
# 'n_estimators': [50, 60, 70, 80,90,100,110],
    'n_estimators': [50, 60,],
    'learning_rate':[0.3,0.5],
    # 'learning_rate': [0.3, 0.5, 0.6, 0.7],
    'max_depth':[3,5],
    # 'max_depth': [3, 5, 6, 7, 8, 9],
}
estimator3= GradientBoostingClassifier()
estimator3.fit(x_train, y_train)

estimator4 = GridSearchCV(estimator3, param_dict, cv = 5)
estimator4.fit(x_train, y_train)
print(f'网格搜索后的模型准确率为：{estimator4.best_score_}')
print(f'网格搜索后的模型为：{estimator4.best_params_}')

