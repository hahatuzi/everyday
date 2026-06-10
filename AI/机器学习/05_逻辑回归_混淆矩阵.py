import pandas
import pandas as pd
from scipy.constants import precision
from sklearn.metrics import confusion_matrix, precision_score

# 10个样本，6个恶性，4个良性
# 模型A：预测对了3个恶性，3个良性
# 模型B：预测对了6个恶性，1个良性
# 1.定义样本
y_train = ['恶性','恶性','恶性','恶性','恶性','恶性','良性','良性','良性','良性']
y_train_A = ['恶性','恶性','恶性','良性','良性','良性','良性','良性','良性','良性']
y_train_B = ['恶性','恶性','恶性','恶性','恶性','恶性','良性','恶性','恶性','恶性']

# 2.针对真实结果和预测结果搭建混淆矩阵
cm_A = confusion_matrix(y_train, y_train_A)
print(f'混淆矩阵A:\n{cm_A}')
df_A = pandas.DataFrame(cm_A)
print(f'混淆矩阵A:\n{df_A}')

cm_B = confusion_matrix(y_train, y_train_B)
print(f'混淆矩阵A:\n{cm_B}')
df_B = pandas.DataFrame(cm_B)
print(f'混淆矩阵A:\n{df_B}')
# [[3 3] [1 3]]
# 计算模型的精确率和召回率
labels = ['恶性', '良性']
print(f'混淆矩阵A的精确率:\n{precision_score(y_train, y_train_A, pos_label='恶性')}')
