from sklearn.preprocessing import MinMaxScaler
x_train = [[90,2,10,40],[60,4,15,45],[75,3,13,46]]
transfer = MinMaxScaler(feature_range=(0,1))
x_train_new = transfer.fit_transform(x_train)
print(x_train_new)