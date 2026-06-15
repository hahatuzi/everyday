# Baggind思想
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
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
x['Age'] = x['Age'].fillna(x['Age'].mean())
# 2.3 热编码处理
x = pd.get_dummies(x, columns=['Sex'])
print(x)
print(y)
# 2.4 划分训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size= 0.2,random_state=23)

# 4.模型训练
estimator = DecisionTreeClassifier()
estimator.fit(x_train, y_train)
# 模型预测
y_pred = estimator.predict(x_test)
print(f'预测结果1为：{estimator.score(x_test, y_test)}')


estimator2 = RandomForestClassifier()
estimator2.fit(x_train, y_train)
y_pred2 = estimator2.predict(x_test)
print(f'预测准确率2为：{estimator2.score(x_test, y_test)}')


estimator3 = RandomForestClassifier()
estimator3.fit(x_train, y_train)
params = {'n_estimators':[30,50,60,90,130],'max_depth':[2,3,5,7]}
gs_estimator = GridSearchCV(estimator3, param_grid=params, cv=2)
gs_estimator.fit(x_train, y_train)
y_pred3 = gs_estimator.predict(x_test)
print(f'预测准确率3为:{estimator3.score(x_test, y_test)}')
print(f'最佳结果为：{gs_estimator.best_params_}')
# Boosting思想
# 使用决策树进行模型训练和评估
# 随机森林进行模型