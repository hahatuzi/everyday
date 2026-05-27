# 1.导包
from sklearn.neighbors import KNeighborsClassifier

# 2.准备测试集和训练集
x_train = [[0],[1],[2],[3]]
y_train = [0,0,1,1]
x_test= [[5]]

# 3.创建KNN模型对象
estimator = KNeighborsClassifier(n_neighbors=2)
# 4.模型训练
estimator.fit(x_train, y_train)
# 5.模型预测
y_test = estimator.predict(x_test)
# print(f'预测值为:{y_test}')
print('预测值为', y_test)