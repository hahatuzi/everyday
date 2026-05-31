# 鸢尾花测试集
from sklearn.datasets import load_iris
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# 分割测试集和数据集
from sklearn.model_selection import train_test_split, GridSearchCV
# 分类对象
from sklearn.neighbors import KNeighborsClassifier
# 数据标准化
from sklearn.preprocessing import StandardScaler
# 模型评估
from sklearn.metrics import accuracy_score


# 1.定义函数：加载鸢尾花数据集，并察看
def iris_load():
    iris_data = load_iris()
    print(f'数据集为{iris_data}')
    print(f'数据集为{type(iris_data)}')
    print(f'数据集的所有键名为{iris_data.keys()}')
    # 鸢尾花数据集前5条数据
    print(f'数据集的数据集前5条数据为{iris_data.data[:5]}')
    print(f'数据集的标签前5条为{iris_data.target[:5]}')
    print(f'数据集的标签对应的名称为{iris_data.target_names}')
    print(f'数据集的特征对应的名称为{iris_data.feature_names}')
    print(f'数据集的特征对应的文件名为{iris_data.filename}')

# 2.定义函数：绘制数据集的散点图
def show_iris():
    # 第一步：加载数据集
    iris_data = load_iris()
    # 第二步：将数据集封装成DataFrame对象
    iris_df = pd.DataFrame(iris_data.data, columns=iris_data.feature_names)
    # 第三步：给df对象新增一列，label列
    iris_df['label'] = iris_data.target
    # 第四步：通过seaborn绘制散点图
    # print(f'{iris_df}')

    sns.lmplot(data=iris_df, x='sepal length (cm)', y='sepal width (cm)',hue='label',fit_reg=False)
    # 第五步：设置标题，显示
    plt.title('iris data')
    plt.tight_layout()
    plt.show()

# 3.定义函数：切分训练集和测试集
def split_train_test():
    iris_data = load_iris()
    # 第一步：将150个数据集切分成8：2的训练集：测试集
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.2,random_state=100)
    # 第三步：打印切分后的结果
    print(f'训练集的特征{x_train},个数{len(x_train)}')
    print(f'训练集的特征{x_test},个数{len(x_test)}')
    print(f'训练集的特征{y_train},个数{len(y_train)}')
    print(f'训练集的特征{y_test},个数{len(y_test)}')

# 4.定义函数，实现鸢尾花完整案例：数据加载，数据预处理,特征工程
def iris_evaluate_test():
    # 第一步：加载数据
    iris_data = load_iris()
    # 第二步：数据预处理：将150个数据集切分成8：2的训练集：测试集
    x_train,x_test,y_train,y_test = train_test_split(iris_data.data, iris_data.target, test_size=0.25,random_state=40)
    # 第三步：特征工程:特征提取，特征处理
    # 源数据的4列特征差别不大，可以不处理，但加入更加完善
    transfer = StandardScaler()
    # fit_rtansform兼顾训练和转换，适用于第一次进行标准化的时候
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)
    # 第四步：模型训练
    estimator = KNeighborsClassifier(n_neighbors=3)
    estimator.fit(x_train,y_train)
    # 第五步：模型预测
    #     5-1:对30条测试
    y_pre = estimator.predict(x_test)
    print(f'预测值为{y_pre}')
    #     5-2:对150条以外的新数据进行预测
    my_data = [[7.8,2.1,3.9,1.6]]
    my_data = transfer.transform(my_data)
    y_pre_new = estimator.predict(my_data)
    print(f'新的预测值为{y_pre_new}')
    #     5-3查看上述数据集，每种分类的预测概率
    y_pre_prob = estimator.predict_proba(my_data)
    print(f'各个分类的预测概率为{y_pre_prob}')
    # 6.模型评分
    # 6-1:直接评分，基于训练集和测试集
    print(f'正确率为{estimator.score(x_train,y_train)}') # 0.95
    # 6-2：基于测试集的标签和预测结果进行评分
    print(f'正确率为{accuracy_score(y_test,y_pre)}') # 1.0

if __name__ == '__main__':
    # iris_load()
    # show_iris()
    # split_train_test()
    iris_evaluate_test()