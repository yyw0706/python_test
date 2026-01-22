from sklearn.utils import shuffle
import torch
import torch.nn as nn
import torch.optim as optim
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

data = pd.read_csv("train.csv")
print("Train_data")
data.info()
# 需要先进行数据清洗
# 删除列，axis=1表示按列
data.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1, inplace=True)
# fillna() 是 pandas 库中用于处理缺失值（如 NaN）的核心方法，它允许你用指定值或策略填充 DataFrame 或 Series 中的空值
# mode() 是DataFrame或Series对象的方法，用于沿指定轴计算众数
data["Age"].fillna(data["Age"].mean(), inplace=True)
data["Embarked"].fillna(data["Embarked"].mode()[0], inplace=True)
# LabelEncoder 是scikit-learn 库中用于将分类标签转换为数值形式的工具，它将每个唯一的类别映射为
# 一个整数（从 0 到 n_classes-1），从而将文本或非数值数据转换为机器学习算法可以处理的数值格式
le = LabelEncoder()
# fit_transform() 是 Scikit-learn 库中数据预处理转换器的核心方法，用于先拟合数据计算统计参数
# （如均值、方差），再应用这些参数对数据进行标准化、归一化等转换操作，通常仅用于训练集
data["Sex"] = le.fit_transform(data["Sex"])
data["Embarked"] = le.fit_transform(data["Embarked"])
# x数据表示除Survived列之外的数据，y数据表示只有Survived列
X = data.drop("Survived", axis=1)
y = data["Survived"]
# StandardScaler是scikit-learn库中preprocessing模块提供的一个类，用于实现特征标准化
# （也称为Z-score标准化），其核心目标是将每个特征缩放到均值为0、标准差为1的标准正态分布，
# 从而消除不同特征之间的量纲差异，使数据更适合后续的机器学习算法
scaler = StandardScaler()
X = scaler.fit_transform(X)

test_Data = pd.read_csv("test.csv")
print("Test_data")
test_Data.info()
y_test_data_0 = test_Data["PassengerId"]
# to_numpy() 是 Pandas 库中用于将 DataFrame 或 Series 转换为 NumPy 数组的方法
y_test_data_0 = y_test_data_0.to_numpy()
test_Data.drop(["PassengerId", "Name", "Ticket", "Cabin"], axis=1, inplace=True)
test_Data["Age"].fillna(data["Age"].mean(), inplace=True)
test_Data["Embarked"].fillna(test_Data["Embarked"].mode()[0], inplace=True)
le = LabelEncoder()
test_Data["Sex"] = le.fit_transform(test_Data["Sex"])
test_Data["Embarked"] = le.fit_transform(test_Data["Embarked"])
scaler = StandardScaler()
x_test_Data = scaler.fit_transform(test_Data)
x_test_Data = torch.from_numpy(x_test_Data).float()

# 将数据集分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# 将数据转换为张量
X_train = torch.from_numpy(X_train).float()
X_test = torch.from_numpy(X_test).float()
y_train = torch.from_numpy(y_train.to_numpy()).float()
y_test = torch.from_numpy(y_test.to_numpy()).float()
print(X_train)
print(y_train)
print(data)
X = torch.from_numpy(X).float()
y = torch.from_numpy(y.to_numpy()).float()


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(7, 32)
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 8)
        self.fc4 = nn.Linear(8, 1)
        self.dropout = nn.Dropout(0.2)
        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.relu(self.fc3(x))
        x = self.dropout(x)
        x = self.sigmoid(self.fc4(x))
        return x


model = Net()

criterion = nn.BCELoss(reduction='sum')
optimizer = optim.Adam(model.parameters(), weight_decay=0.01)

# 训练模型
epochs = 50
batch_size = 32
for epoch in range(epochs):
    running_loss = 0.0
    X_train, y_train = shuffle(X_train, y_train)
    for i in range(0, len(X_train), batch_size):
        inputs = X_train[i:i + batch_size]
        labels = y_train[i:i + batch_size]
        outputs = model(inputs)
        loss = criterion(outputs.squeeze(), labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch + 1}, loss: {running_loss / len(X_train)}")

with torch.no_grad():
    outputs = model(X_test)
    outputs = outputs.squeeze()
    outputs[outputs >= 0.5] = 1.0
    outputs[outputs < 0.5] = 0.0
    accuracy = torch.sum(outputs == y_test) / len(y_test)
    print("Test accuracy:", accuracy.item())

print("正式训练开始")
for epoch in range(1000):
    running_loss = 0.0
    for i in range(0, len(X), batch_size):
        inputs = X[i:i + batch_size]
        labels = y[i:i + batch_size]
        # 梯度清零
        optimizer.zero_grad()
        outputs = model(inputs)
        # 计算损失
        loss = criterion(outputs.squeeze(), labels)
        # 反向传播
        loss.backward()
        # 梯度更新
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch + 1}, loss: {running_loss / len(X)}")

y_test_data = model(x_test_Data)
y_test_data = y_test_data.detach().numpy()
y_test_data = (y_test_data >= 0.5).astype(np.int32)
print(y_test_data)
print(y_test_data_0)
y_test_data = y_test_data.squeeze()
y_test_data_0 = y_test_data_0.tolist()
y_test_data = y_test_data.tolist()
df = pd.DataFrame({"PassengerId": y_test_data_0, "Survived": y_test_data})

df.to_csv("gender_submission.csv")
