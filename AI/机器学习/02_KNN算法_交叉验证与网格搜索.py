"""
数据分成n份
第1份作为验证集，其他为训练集，准确率为1
第2份作为验证集，其他为训练集，准确率为2
第3份作为验证集，其他为训练集，准确率为3
第4份作为验证集，其他为训练集，准确率为4
取上述4份的平均值，作为模型的最终准确率
假设第4份准确率最高，再用全部数据作为训练集，第4份作为测试集
"""
# 鸢尾花测试集
from sklearn.datasets import load_iris
# 分割测试集和数据集,寻找最优超参
from sklearn.model_selection import train_test_split,GridSearchCV
# 分类对象
from sklearn.neighbors import KNeighborsClassifier
# 数据标准化
from sklearn.preprocessing import StandardScaler
# 模型评估
from sklearn.metrics import accuracy_score
iris_data = load_iris()
x_train,x_test,y_train,y_test = train_test_split(iris_data.data,iris_data.target,test_size=0.2,random_state=22)
transfer = StandardScaler()
x_train = transfer.fit_transform(x_train)
x_test = transfer.transform(x_test)
estimator = KNeighborsClassifier()
param_dict = {'n_neighbors':[i for i in range(1,11)]}
estimator = GridSearchCV(estimator=estimator,param_grid=param_dict,cv=4)
estimator.fit(x_train,y_train)
print(estimator.best_params_)
print(estimator.best_score_)
print(estimator.best_estimator_)
