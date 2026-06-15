# Baggind思想
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report


# 1.加载数据
data = pd.read_csv('./data/红酒品质分类.csv')
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


