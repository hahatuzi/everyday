from sklearn.preprocessing import StandardScaler
x_train = [[90,2,10,40],[60,4,15,45],[75,3,13,46]]
transfer = StandardScaler()
x_train_new = transfer.fit_transform(x_train)
print(x_train_new)
print(f'方差为：{transfer.var_}')
print(f'均值为：{transfer.mean_}')
print(f'标准差为：{transfer.scale_}')
