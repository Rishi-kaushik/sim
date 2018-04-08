import math
import random
import sqlite3
import copy


class Node:
    def __init__(self, width):
        self.in_weights = []
        self.bias = random.gauss(0, 1)
        self.value = 0
        self.delta = 0
        self.acc = 0
        for i in range(0, width):
            self.in_weights.append(random.gauss(0, 1.25))

    def evaluate(self, last_layer):
        self.value = self.bias
        for i in range(0, len(self.in_weights)):
            self.value += last_layer.nodes[i].val * self.in_weights[i]
        if self.value < 0:  # RELU for non-linearity
            self.value = 0


class Layer:
    def __init__(self, width, last_layer=None):
        self.nodes = []
        for i in range(0, width):
            if last_layer is not None:
                self.nodes.append(Node(len(last_layer.nodes)))
            else:
                self.nodes.append(Node(0))

    def evaluate(self, last_layer):
        for i in range(0, len(self.nodes)):
            self.nodes[i].evaluate(last_layer)

    def value(self):
        a = []
        for i in range(len(self.nodes)):
            a.append(self.nodes[i].value)
        return a


class Network:
    def __init__(self, rate=.01, error=.001):
        self.default_rate = rate
        self.default_error = error
        self.layer = []
        self.depth = 0
        self.reset()  # not req

    def reset(self):  # to reset the record to all zeros
        for i in range(0, len(self.layer)):
            for j in range(0, len(self.layer[i])):
                self.layer[i].nodes[j].value = 0
                self.layer[i].nodes[j].delta = 0
                self.layer[i].nodes[j].acc = 0

    def add_layer(self, width):
        if len(self.layer) != 0:
            self.layer.append(Layer(width, self.layer[-1]))
        else:
            self.layer.append(Layer(width))

    def evaluate(self, input_vals: []):
        for i in range(0, len(self.layer[0])):
            self.layer[0].nodes[i].value = input_vals[i]
        for i in range(1, len(self.layer)):
            self.layer[i].evaluate(self.layer[i - 1])
        # self.out_node.evaluate(self.layer[-1])
        # if store:
        #     self.batch_size += 1
        #     for i in range(0, self.depth):
        #         for j in range(0, self.width):
        #             self.record[i][j] += self.layer[i].nodes[j].value
        return self.layer[-1].value()

    def store(self, true_output):
        for i in range(len(self.layer[-1])):
            self.layer[-1].nodes[i].delta += true_output[i] - self.layer[-1].nodes[i].value
            self.layer[-1].nodes[i].acc += self.layer[-1].nodes[i].value
        for i in range(len(self.layer) - 2, 0, -1):
            for j in range(len(self.layer[i])):
                self.layer[i].nodes[j].acc += self.layer[i].nodes[j].value
                for k in range(len(self.layer[i + 1])):
                    self.layer[i].nodes[j].delta += self.layer[i + 1].nodes[k].delta * self.layer[i + 1].nodes[k].in_weights[j]
        return

    def learn_data(self, input_data: list = None, output_data: list = None, batch_size: int = 0, learning_rate: int = 0, tagget_error: int = 0):
        if input_data is None or output_data is None or len(input_data) is 0 or len(output_data) is 0:
            return
        # data = sqlite3.connect(input_data)
        if len(input_data[0]) == len(self.layer[0]) and len(output_data[0]) == len(self.layer[-1]):
            self.reset()
            if learning_rate is 0:
                learning_rate = self.default_rate
            if batch_size is 0:
                batch_size = len(input_data)
            if tagget_error is 0:
                tagget_error = self.default_error
            error = 1
            while error > tagget_error:
                start = random.randint(0, len(input_data) - 1 - batch_size)
                for i in range(start, start + batch_size):
                    self.evaluate(input_data[i])
                    self.store(output_data[i])
                self.learn()
                error = 0
                for i in range(len(self.layer[-1])):
                    error += math.pow(self.layer[-1].nodes[i].delta,2)
                error = math.pow(error/batch_size,0.5)
        else:
            return 0

    def learn(self):  # error = desired - obtained
        #To be cont........
        rec = copy.deepcopy(self.record)
        for i in range(self.depth):
            for j in range(self.width):
                self.record[i][j] /= self.batch_size

        self.out_node.bias += error * self.default_rate
        for i in range(self.width):
            self.out_node.in_weights[i] += error * self.record[-1][i] * self.default_rate

        deltas = []
        l = []
        for i in range(self.width):
            l.append(0)
            if self.layer[-1].nodes[i].value > 0:
                l[i] += error * self.out_node.in_weights[i]
        deltas.insert(0, l)
        for i in range(2, self.depth):
            l = []
            for j in range(self.width):
                l.append(0)
                if self.layer[-i].nodes[j].value > 0:
                    for k in range(self.width):
                        l[j] += deltas[0][k] * self.layer[-i + 1].nodes[k].in_weights[j]
            deltas.insert(0, l)

        for i in range(1, self.depth):
            for j in range(self.width):
                self.layer[-i].nodes[j].bias += deltas[-i][j] * self.default_rate
                for k in range(self.width):
                    self.layer[-i].nodes[j].in_weights[k] += deltas[-i][j] * self.record[-i - 1][k] * self.default_rate
        self.record = rec

    @property
    def __str__(self):
        out_str = ''
        for i in range(0, len(self.layer)):
            for j in range(0, len(self.layer[i].nodes)):
                out_str += '  ' + str(self.layer[i].nodes[j].bias)
            out_str += '\n'
        return out_str


net = Network(0.01)
net.add_layer(4)
net.add_layer(6)
net.add_layer(6)
net.add_layer(2)

a = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0]
]
ans = [
    0,
    1,
    1,
    0
]
# # print(net)
#
# for k in range(10000):
#     for i in range(len(a)):
#         x = net.evaluate(a[i])
#         err = ans[i] - x
#         net.learn(err)
#         net.reset()
#
# test = [
#     [0, 0, 0, 0],
#     [0, 1, 0, 0],
#     [1, 0, 0, 0],
#     [1, 1, 0, 0]
# ]
# for i in range(len(test)):
#     x = net.evaluate(test[i])
#     print(x)
# # print("\n\n\n\n\n\n\n\n\n\n")
print(net.__str__)
