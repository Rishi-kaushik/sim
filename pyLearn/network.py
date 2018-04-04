import random
import sqlite3
import copy


class Node:
    def __init__(self, width):
        self.in_weights = []
        self.bias = random.gauss(0, 1)
        self.val = 0
        for i in range(0, width):
            self.in_weights.append(random.gauss(0, 1.25))

    def evaluate(self, last_layer):
        self.val = self.bias
        for i in range(0, len(self.in_weights)):
            self.val += last_layer.nodes[i].val * self.in_weights[i]
        if self.val < 0:  # RELU for non-linearity
            self.val = 0


class Layer:
    def __init__(self, width):
        self.nodes = []
        for i in range(0, width):
            self.nodes.append(Node(width))

    def evaluate(self, last_layer):
        for i in range(0, len(self.nodes)):
            self.nodes[i].evaluate(last_layer)


class Network:
    def __init__(self, width, depth, rate=.01):
        self.rate = rate
        self.width = width
        self.depth = depth
        self.out_node = Node(self.width)
        self.layers = []
        self.record = []
        self.batch_size = 0
        for i in range(0, self.depth):
            self.layers.append(Layer(self.width))
            l = []
            for j in range(0, self.width):
                l.append(0)
            self.record.append(l)
        self.reset()  # not req

    def reset(self):  # to reset the record to all zeros
        self.batch_size = 0
        for i in range(0, len(self.record)):
            for j in range(0, len(self.record[i])):
                self.record[i][j] = 0

    def evaluate(self, input_vals: [], store: bool = True):
        for i in range(0, self.width):
            self.layers[0].nodes[i].val = input_vals[i]
        for i in range(1, self.depth):
            self.layers[i].evaluate(self.layers[i - 1])
        self.out_node.evaluate(self.layers[-1])
        if store:
            self.batch_size += 1
            for i in range(0, self.depth):
                for j in range(0, self.width):
                    self.record[i][j] += self.layers[i].nodes[j].val
        return self.out_node.val

    def learn_data(self, input_data: str = None):  # felt lazy......plus didnt needed it.....
        if input_data is None:
            return
        data = sqlite3.connect(input_data)

    def learn(self, error: int):  # error = desired - obtained

        rec = copy.deepcopy(self.record)
        for i in range(self.depth):
            for j in range(self.width):
                self.record[i][j] /= self.batch_size

        self.out_node.bias += error * self.rate
        for i in range(self.width):
            self.out_node.in_weights[i] += error * self.record[-1][i] * self.rate

        deltas = []
        l = []
        for i in range(self.width):
            l.append(0)
            if self.layers[-1].nodes[i].val > 0:
                l[i] += error * self.out_node.in_weights[i]
        deltas.insert(0, l)
        for i in range(2, self.depth):
            l = []
            for j in range(self.width):
                l.append(0)
                if self.layers[-i].nodes[j].val > 0:
                    for k in range(self.width):
                        l[j] += deltas[0][k] * self.layers[-i + 1].nodes[k].in_weights[j]
            deltas.insert(0, l)

        for i in range(1, self.depth):
            for j in range(self.width):
                self.layers[-i].nodes[j].bias += deltas[-i][j] * self.rate
                for k in range(self.width):
                    self.layers[-i].nodes[j].in_weights[k] += deltas[-i][j] * self.record[-i - 1][k] * self.rate
        self.record = rec

    @property
    def __str__(self):
        out_str = ''
        for i in range(0, self.depth):
            for j in range(0, self.width):
                out_str += '  ' + str(self.layers[j].nodes[i].val)
            out_str += '\n'
        return out_str


net = Network(4, 3, 0.01)
a = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0]
]
ans = [0, 1, 1, 0]
# print(net)

for k in range(10000):
    for i in range(len(a)):
        x = net.evaluate(a[i])
        err = ans[i] - x
        net.learn(err)
        net.reset()

test = [
    [0, 0, 0, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 0, 0]
]
for i in range(len(test)):
    x = net.evaluate(test[i])
    print(x)
# print(net)
