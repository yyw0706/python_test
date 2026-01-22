# @Auther   :Mateo
import torch
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torch.optim as optim

batch_size = 64
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(root='../dataset/minist',
                               train=True,
                               download=True,
                               transform=transform)
train_loader = DataLoader(train_dataset,
                          shuffle=True,
                          batch_size=batch_size)
test_dataset = datasets.MNIST(root='../dataset/minist',
                              train=False,
                              download=True,
                              transform=transform)
test_loader = DataLoader(test_dataset,
                         shuffle=False,
                         batch_size=batch_size)


class Net(torch.nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)
        self.pooling = torch.nn.MaxPool2d(2)
        self.fc = torch.nn.Linear(320, 10)

    def forward(self, x):
        batch_size = x.size(0)
        x = F.relu(self.pooling(self.conv1(x)))
        x = F.relu(self.pooling(self.conv2(x)))
        x = x.view(batch_size, -1)
        x = self.fc(x)
        return x


model = Net()
criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.1, momentum=0.5)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device)


def train(epoch):
    running_loss = 0.0
    for batch_idx, data in enumerate(train_loader, 0):
        inputs, target = data
        optimizer.zero_grad()

        outputs = model(inputs)
        loss = criterion(outputs, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_idx % 300 == 299:
            # %d：十进制整数占位符,%5d：宽度为5的右对齐整数（不足5位时左侧补空格),%.3f：保留3位小数的浮点数
            # 通过(epoch + 1, batch_idx + 1, running_loss / 2000)提供具体值：
            # %d → epoch + 1
            # 将当前训练轮次epoch（通常从0开始计数）加1后显示，例如epoch=0时显示1
            # %5d → batch_idx + 1
            # 将当前批次索引batch_idx加1后显示，并保证总宽度为5位（如batch_idx=3时显示 4）
            # %.3f → running_loss / 2000
            # 计算平均损失值（running_loss可能是累计损失，除以2000得到平均值），保留3位小数
            print('[%d,%5d] loss: %.3f' % (epoch + 1, batch_idx + 1, running_loss / 2000))
            running_loss = 0.0


def test():
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            inputs, target = data
            outputs = model(inputs)
            _, predicted = torch.max(outputs.data, dim=1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
    # Accuracy on test set:：固定文本，表示输出内容为测试集准确率
    # %d：第一个占位符，用于显示准确率的百分比数值（整数）
    # %%：转义后的百分号字符（%符号需用两个%表示）
    # [%d/%d]：包含两个占位符的括号结构，分别显示正确预测的样本数和总样本数
    # 通过(100 * correct / total, correct, total)提供具体值：
    # %d → 100 * correct / total  [%d/%d] → (correct, total)直接显示原始数据：[正确样本数/总样本数]
    print('Accuracy on test set: %d %% [%d/%d]' % (100 * correct / total, correct, total))


if __name__ == '__main__':
    for epoch in range(10):
        train(epoch)
        test()
