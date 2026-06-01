from sklearn.linear_model import LinearRegression
x_train = [[160],[166],[172],[174],[180]]
y_train = [[56.3],[60.5],[65.1],[65.8],[75]]
_test = [[176]]
estimator = LinearRegression()
estimator.fit(x_train,y_train)
print(estimator.coef_)
print(estimator.intercept_)
y_pre = estimator.predict(_test)
print(f'预测值为{y_pre}')