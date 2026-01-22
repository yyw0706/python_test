# @Auther   :Mateo
import torch
import numpy as np
from torch.utils.data import Dataset
from torch.utils.data import DataLoader


# prepare dataset
class DiabetesDataset(Dataset):
    def __init__(self, filepath):
        xy = np.loadtxt(filepath, delimiter=',', dtype=np.float32)  # (759, 9) 最后一列是标签，二分类0,1
        self.len = xy.shape[0]
        self.x_data = torch.from_numpy(xy[:, :-1])  # 获取样本特征
        self.y_data = torch.from_numpy(xy[:, [-1]])  # 获取样本标签

    def __getitem__(self, index):  # 获取样本索引
        return self.x_data[index], self.y_data[index]

    def __len__(self):  # 获取样本总量：759
        return self.len


dataset = DiabetesDataset('diabetes.csv')
train_loader = DataLoader(dataset=dataset, batch_size=64, shuffle=False, num_workers=4)  # num_workers：多进程数据加载


# design model using class
class Model(torch.nn.Module):
    def __init__(self):
        super(Model, self).__init__()
        self.linear1 = torch.nn.Linear(8, 6)
        self.linear2 = torch.nn.Linear(6, 4)
        self.linear3 = torch.nn.Linear(4, 1)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        x = self.sigmoid(self.linear3(x))
        return x


model = Model()

# construct loss and optimizer
criterion = torch.nn.BCELoss(reduction='mean')
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

# training cycle forward, backward, update
if __name__ == '__main__':
    for epoch in range(1):
        for i, data in enumerate(train_loader, 0):  # 迭代对象
            inputs, labels = data
            print(len(data[0]))
            y_pred = model(inputs)
            loss = criterion(y_pred, labels)
            print(epoch, i, loss.item())

            optimizer.zero_grad()
            loss.backward()

            optimizer.step()
