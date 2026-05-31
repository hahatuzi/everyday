from sklearn.datasets import load_iris
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# 分割测试集和数据集
from sklearn.model_selection import train_test_split
# 分类对象
from sklearn.neighbors import KNeighborsClassifier
# 数据标准化
from sklearn.preprocessing import StandardScaler
# 模型评估
from sklearn.metrics import accuracy_score


# 1.定义函数，接收用户传入的索引，展示手写数字.csv文件中该索引对应的数字
def show_digit(index):
    df = pd.read_csv('./data/手写数字.csv')
    if index < 0 or index >= len(df) - 1
        print('索引越界')
        return
    x = df.iloc[:,1:]
    y = df.iloc[:,0]
    print(f('y'))
    x = x.iloc[index].values.reshape(28,28)
    plt.imshow(x,cmap='gray')
    plt.axis('off')
    plt.show()
# 2.判断用户传入的数字是否越界
# 3.
# 4.测试
if__name__ == '__main__':
show_digit()

def use_model():
  x = plt.imread('./data/iris.jpg')