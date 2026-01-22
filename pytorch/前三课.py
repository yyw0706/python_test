# @Auther   :Mateo
# @Auther   :Mateo
import numpy as np
import matplotlib.pyplot as plt
# x_data = [ 1.0 , 2.0 , 3.0]
# y_data = [ 2.0 , 4.0 , 6.0]
# def forward(x):
#     return x * w
# def loss(x, y):
#     y_pred = forward(x)
#     return (y_pred-y) * (y_pred-y)
# w_list = []
# mse_list = []
# for w in np.arange(0.0, 4.1, 0.1):
#     print (' w=',w)
#     l_sum = 0
#     for x_val, y_val in zip(x_data, y_data):
#         y_pred_val = forward(x_val)
#         loss_val = loss(x_val, y_val)
#         l_sum += loss_val
#         print ('\t ', x_val, y_val, y_pred_val, loss_val)
#     print (' MSE=', l_sum / 3)
#     w_list.append(w)
#     mse_list.append(l_sum / 3)
#
# plt.plot(w_list, mse_list)
# plt.ylabel('Loss')
# plt.xlabel('w')
# plt.show()

x_data = [1.0 , 2.0 , 3.0]
y_data = [ 2.0 , 4.0 , 6.0]
w = 1.0
def forward(x):
    return x * w
def cost(xs, ys):
    cost = 0
    for x, y in zip (xs,ys):
        y_pred = forward(x)
        cost += (y_pred-y) ** 2
    return cost / len(xs)
def gradient(xs, ys):
    grad = 0
    for x, y in zip(xs,ys):
        grad += 2 * x * (x * w-y)
    return grad / len(xs)
print('Predict (before training)', 4 , forward(4))
for epoch in range(100):
    cost_val = cost(x_data, y_data)
    grad_val = gradient(x_data, y_data)
    w -= 0.01 * grad_val
    print(' Epoch:', epoch, ' w=', round(w,2), ' loss=', round(cost_val,2))
print('Predict (after training)', 4, forward(4))

plt.plot(epoch, round(cost_val,2))
plt.ylabel('cost')
plt.xlabel('epoch')
plt.show()

