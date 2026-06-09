import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from sklearn.tree import plot_tree

# 欠拟合
def under_fitting():
    np.random.seed(23)
    x = np.random.uniform(-3, 3, size=100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0,1,size=100)
    print(f'特征(x):{x}')
    print(f'特征(y):{y}')

    X = x.reshape(-1,1)
    print(f'处理后的数据为{X[:5]}')
    # 正规方程，线性回归模型
    estimator = LinearRegression()
    # estimator = Lasso(alpha=0.1)
    estimator.fit(X,y)
    y_predict = estimator.predict(X)
    print(f'均方误差为{mean_squared_error(y,y_predict)}')
    plt.scatter(X,y)
    plt.plot(X,y_predict,color='red')
    plt.show()


# 正好拟合
def just_fitting():
    np.random.seed(23)
    x = np.random.uniform(-3, 3, size=100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, size=100)
    print(f'特征(x):{x}')
    print(f'特征(y):{y}')

    X = x.reshape(-1,1)
    X2 = np.hstack([X , X ** 2])
    print(f'处理后的数据为{X2[:5]}')

    estimator = LinearRegression()
    estimator.fit(X2, y)
    y_predict = estimator.predict(X2)
    print(f'均方误差为{mean_squared_error(y, y_predict)}')
    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='red')
    plt.show()

# 过拟合
def over_fitting():
    np.random.seed(23)
    x = np.random.uniform(-3, 3, size=100)
    y = 0.5 * x ** 2 + x + 2 + np.random.normal(0, 1, size=100)
    print(f'特征(x):{x}')
    print(f'特征(y):{y}')

    X = x.reshape(-1,1)
    X3 = np.hstack([X , X ** 2, X ** 3, X ** 4, X ** 5, X ** 6, X ** 7, X ** 8, X ** 9])
    print(f'处理后的数据为{X3[:5]}')

    # estimator = LinearRegression()
    estimator = Ridge(alpha=0.1)
    estimator.fit(X3, y)
    y_predict = estimator.predict(X3)
    print(f'均方误差为{mean_squared_error(y, y_predict)}')
    plt.scatter(x, y)
    plt.plot(np.sort(x), y_predict[np.argsort(x)], color='red')
    plt.show()

if __name__ == '__main__':
    # under_fitting()
    # just_fitting()
    over_fitting()